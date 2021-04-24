import pandas as pd
import os
from defusedxml.ElementTree import parse
from .coordinates import CoordinateSystem
from .coordinates import UtmCoordinate


class Survey():
    """
    The survey class is the starting point of this library
    Its data source is expected to represent a collection of points within a
    cartesian coordinate system.
    """

    def __init__(
        self,
        source,
        name='Survey',
        coordinate_system=CoordinateSystem.CARTESIAN):
        """Initializes a survey object

        :param source: path to the file that contains the survey data.
                       Accepted file types: .txt, .csv, .gpx
        :param name: a meaningful name for this survey (str).
                     Default: 'Survey'
        :param coordinate_system: an enumeration based on available coordinate
                                  systems at the coordinates module.
                                  Default: CoordinateSystem.CARTESIAN

        :attr data: pandas DataFrame containing x, y, z, elevation as columns.
                    internally set according to the available source file and
                    CoordinateSystem.
        """

        # Validate if extension is supported.
        (_, extension) = os.path.splitext(source)
        accepted_extensions = set(['.gpx','.csv', '.txt'])
        extension = extension.lower()
        if extension not in accepted_extensions:
            raise TypeError(
                "The file extension provided is not currently supported.")

        # initialize class
        self.name = name
        self.source = source
        self.coordinate_system = coordinate_system

        if extension == '.gpx':
            self.data = self._read_gpx()
        elif (extension == '.csv') or (extension == '.txt'):
            expected_col_names = {
                CoordinateSystem.GEOGRAPHIC: ['latitude',
                                              'longitude',
                                              'elevation',],
                CoordinateSystem.UTM: ['northing',
                                       'easting',
                                       'elevation',],
                CoordinateSystem.CARTESIAN: ['x',
                                             'y',
                                             'z',]
            }
            self.data = self._read_txt(
                expected_col_names[self.coordinate_system])
        else:
            raise ValueError("Error while parsing supported file extension.")

    def get_bounds(self):
        """
        Returns a tuple with the maximum values for x, y, z available on the
        survey data
        """
        x_max = self.data['x'].max()
        y_max = self.data['y'].max()
        z_max = self.data['z'].max()
        print("x={}; y={}; z={}".format(x_max, y_max, z_max))
        return (x_max, y_max, z_max)

    def _read_gpx(self):
        """Parses an xml file containing GPS data
        Data points are assumed to be in a Geographic coordinate system

        Returns a pandas DataFrame containing the parsed GPS data if parse was
        successful and None otherwise.
        """

        # Parsing XML file
        elements = parse(self.source)
        points = []
        for element in elements.iter():
            if element.tag.find("trkpt") == -1:
                continue

            latitude = element.attrib.get("lat", None)
            longitude = element.attrib.get("lon", None)
            elevation = element[0].text

            if (not latitude or
                not longitude or
                not elevation):
                raise ValueError("Unexpected tag for lat/lon/ele.")

            try:
                latitude = pd.to_numeric(latitude)
                longitude = pd.to_numeric(longitude)
                elevation = pd.to_numeric(elevation)
                utm = UtmCoordinate.create_from_geographic(
                    latitude,
                    longitude,
                    elevation)
                entry = (latitude,
                        longitude,
                        utm.elevation,
                        utm.northing,
                        utm.easting)
                points.append(entry)
            except Exception as exception:
                raise exception

        if len(points) == 0:
            raise(ValueError("Unable to find valid points within the provided GPX file."))

        # Generate DataFrame
        columns = ['latitude',
                   'longitude',
                   'elevation',
                   'northing',
                   'easting']
        data = pd.DataFrame.from_records(points,
                                         columns=columns)

        # Generate x, y, z
        data['x'] = data['easting'] - data['easting'].min()
        data['y'] = data['northing'] - data['northing'].min()
        data['z'] = data['elevation'] - data['elevation'].min()
        selection = ['x', 'y', 'z', 'elevation']
        return data[selection]

    def _read_txt(self, expected_col_names):
        """
        Reads data in txt or csv formats

        Arguments:
        expected_col_names: an array containing the names of the expected column
                            values

        Returns a pandas data frame containing x, y, z, elevation columns
        """

        try:
            # Read data
            data = pd.read_csv(self.source)

            # Check number of columns
            if data.shape[1] != len(expected_col_names):
                    raise ValueError(
                        "Unexpected number of columns. Expected {}.".format(
                            len(expected_col_names)))
            # Check column names
            for item in data.columns:
                if item not in expected_col_names:
                    raise ValueError("Unexpected column name. Expected:{}"\
                        .format(expected_col_names))

            # Convert data
            for column in data.columns:
                data[column] = pd.to_numeric(data[column])

            # Generate output
            if self.coordinate_system == CoordinateSystem.GEOGRAPHIC:
                def generate_utm(row):
                    return UtmCoordinate.create_from_geographic(
                        row['latitude'],
                        row['longitude'],
                        row['elevation'])
                data['UTM'] = data.apply(generate_utm, axis=1)
                data['easting'] = data.apply(lambda row: row['UTM'].easting,
                                             axis=1)
                data['northing'] = data.apply(lambda row: row['UTM'].northing,
                                              axis=1)
                data['x'] = data['easting'] - data['easting'].min()
                data['y'] = data['northing'] - data['northing'].min()
                data['z'] = data['elevation'] - data['elevation'].min()

            elif self.coordinate_system == CoordinateSystem.UTM:
                data['x'] = data['easting'] - data['easting'].min()
                data['y'] = data['northing'] - data['northing'].min()
                data['z'] = data['elevation'] - data['elevation'].min()

            elif self.coordinate_system == CoordinateSystem.CARTESIAN:
                data['elevation'] = data['z'] # keeping return values consitent
                data['z'] = data['elevation'] - data['elevation'].min()

            else:
                raise ValueError('Unknown coordinate system.')

            selection = ['x', 'y', 'z', 'elevation']
            return data[selection]
        except Exception as exception:
            raise exception
