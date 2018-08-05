# Defines the different types of coordinates that application can work with
import utm

class GeographicCoordinate():
    def __init__(self, latitude, longitude, elevation):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation # above sea level

class UtmCoordinate():
    def __init__(self, northing, easting, zone_number, zone_letter, elevation):
        self.northing = northing
        self.easting = easting
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.elevation = elevation

    @classmethod
    def create_from_geographic(cls, latitude, longitude, elevation):
        """ creates an instance in UTM from a geographic coordinate"""
        (northing, easting, zone_number, zone_letter) = utm.from_latlon(
            latitude,
            longitude)
        return cls(northing, easting, zone_number, zone_letter, elevation)

class CartesianCoordinate():
    """
    Classical cartesian coordinate system with x, y, z axes.
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
