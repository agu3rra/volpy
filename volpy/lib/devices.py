import pandas as pd
from enum import Enum
from xml.dom.minidom import parse
import xml.dom.minidom


class GpsDevice(Enum):
    """ An enumeration of previously worked with GPS devices. """
    GARMIN_MONTANA_680 = 0


def read_gpx(filepath, device=GpsDevice.GARMIN_MONTANA_680):
    """
    Parses an xml file containing GPS data for a specific GPS device

    :param filepath: the full path to the file containing XML data to import.
    :param device: an enumeration related to the GPS brand and model since
    different devices can generate data with different structure and tags.

    Returns a pandas DataFrame containing the parsed GPS data if parse was
    successful and None otherwise.
    """
    # Note to future self: consider generalizing if other brand/model devices
    # generate similar XML structure.
    if device == GpsDevice.GARMIN_MONTANA_680:
        dom_tree = xml.dom.minidom.parse(filepath)
        collection = dom_tree.documentElement
        track_points = collection.getElementsByTagName("trkpt")

        points = []

        for point in track_points:
            latitude = point.getAttribute("lat")
            longitude = point.getAttribute("lon")
            elevation = point.getElementsByTagName('ele')[0].childNodes[0].data
            entry = (latitude, longitude, elevation)
            points.append(entry)

        column_names = ["latitude", "longitude", "elevation"]
        return pd.DataFrame.from_records(points,columns=column_names)
    print("Unknown device.")
    return None
