import pandas as pd
import os
from xml.dom.minidom import parse
from coordinates import CoordinateSystem
from coordinates import UtmCoordinate


class Survey():
    """
    The survey class is the starting point of this library
    Its data source is expected to represent a collection of points within a
    cartesian coordinate system.
    """

    def __init__(
        self,
        source,
        name,
        coordinate_system=CoordinateSystem.CARTESIAN):
        """Initializes a survey object

        Arguments:
        source: path to the file that contains the survey data.
                     Accepted file types: .xlsx, .xls, .csv, .gpx
        name: a meaningful name for this survey (str)
        coordinate_system: an enumeration based on available coordinate systems
                           at the coordinates module
        """

        # Validate if extension is supported.
        (_, extension) = os.path.splitext(source)
        accepted_extensions = set(['.xlsx','.xls','.gpx','.csv', '.txt'])
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
            self.data = self._read_csv()
        elif (extension == '.xlsx') or (extension == '.xls'): # MS Excel
            self.data = self._read_excel()
        else:
            raise ValueError("Error while parsing supported file extension.")

    def _pdSeries_conversion(self, series, to):
        """Converts a pandas series to a different dtype
        
        Arguments:
        series: the input pandas series to be converted
        to: the desired data type to convert to in pandas.
            e.g.: float64, object, datetime64

        Returns a pandas Series
        """
        try:
            if (to == "float64" or to == "int64"):
                return pd.to_numeric(series)
            elif to == "datetime64":
                return pd.to_datetime(series)
            elif to == "object":
                return series.to_string()
            else:
                raise TypeError("Unexpected type convertion.")
        except Exception as exception:
            print(exception)
            raise exception

    def _read_gpx(self):
        """Parses an xml file containing GPS data
        Data points are assumed to be in a Geographic coordinate system

        Returns a pandas DataFrame containing the parsed GPS data if parse was
        successful and None otherwise.
        """

        # Parsing XML file
        collection = parse(self.source).documentElement
        track_points = collection.getElementsByTagName("trkpt")
        if len(track_points) == 0:
            raise ValueError("Unexpected trackpoint tag on XML file")
        points = []

        for point in track_points:
            # Parse from XML
            latitude = point.getAttribute("lat")
            longitude = point.getAttribute("lon")
            elevation = point.getElementsByTagName('ele')[0]\
                .childNodes[0].data

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
                                         
    def _read_csv(self):

        if self.coordinate_system == CoordinateSystem.GEOGRAPHIC:
            try:
                contents = pd.read_csv(self.source)
                
                #if contents.shape[1]!=4:
                 #   raise ValueError("Unexpected number of columns")

                # implement reading only time/lat/long/ele as in gpx
                # implement cartesian from the get go. Should have draw it working before implementing it :) All import types should return cartesian.
                # attributes: survey.data = timestamp,x,y,z

                # Verify expected column names
                for item in self._column_names:
                    if item not in contents.columns:
                        raise ValueError("Unexpected column name. Expected:{}"\
                        .format(self._column_names))

                # Convertion to desired dtypes:
                for column in contents.columns:
                    expected_type = self._column_names[column]
                    contents[column] = self._pdSeries_conversion(
                        contents[column],
                        expected_type)
                
                # contents = contents.set_index('timestamp')
                return contents
            except Exception as exception:
                print(exception)
                raise exception

        if self.coordinate_system == CoordinateSystem.CARTESIAN:
            pass

        if self.coordinate_system == CoordinateSystem.UTM:
            pass

    def _read_excel(self):
        return True
