import pandas as pd
import os
from xml.dom.minidom import parse
from coordinates import CoordinateSystem
from coordinates import UtmCoordinate


class Survey():
    """
    The survey class is the starting point of this library
    Its data source is expected to represent a collection of points within a
    cartesian coordinate system
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
        (filename, extension) = os.path.splitext(source)
        accepted_extensions = set(['.xlsx','.xls','.gpx','.csv'])
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
        elif extension == '.csv':
            self.data = self._read_csv()
        elif (extension == '.xlsx') or (extension == '.xls'): # MS Excel
            self.data = self._read_excel()
        else:
            raise IOError("Error while parsing supported file extension.")

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
            raise IOError("Unexpected trackpoint tag on XML file")
        points = []

        for point in track_points:
            # Parse from XML
            latitude = point.getAttribute("lat")
            longitude = point.getAttribute("lon")
            elevation = point.getElementsByTagName('ele')[0]\
                .childNodes[0].data
            timestamp = point.getElementsByTagName('time')[0]\
                .childNodes[0].data

            if (not latitude or
                not longitude or
                not elevation or
                not timestamp):
                raise IOError("Unexpected tag for lat/lon/ele/time.")

            try:
                latitude = pd.to_numeric(latitude)
                longitude = pd.to_numeric(longitude)
                elevation = pd.to_numeric(elevation)
                utm = UtmCoordinate.create_from_geographic(
                    latitude,
                    longitude,
                    elevation)
                timestamp = pd.to_datetime(timestamp)
                entry = (timestamp,
                        latitude,
                        longitude,
                        utm.northing,
                        utm.easting,
                        utm.zone_letter,
                        utm.zone_number,
                        elevation)
                points.append(entry)
            except Exception as exception:
                print(exception)

        # Generate DataFrame
        column_names = ["timestamp",
                        "latitude",
                        "longitude",
                        "northing"
                        "easting",
                        "zone_letter",
                        "zone_number",
                        "elevation"]
        return pd.DataFrame.from_records(points,
                                         columns=column_names,
                                         index="timestamp")
