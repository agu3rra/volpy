from coordinates import CartesianCoordinate

class Line2D():
    """A 2-Dimensional line"""
    def __init__(self,
                 point_A: CartesianCoordinate,
                 point_B: CartesianCoordinate):
        """Constructor
        
        Arguments:
        point_A: Cartesian Coordinate for point A
        point_B: Cartesian Coordinate for point B
        """
        self.point_A = point_A
        self.point_B = point_B
    
    def get_parameters(self):
        """Returns the slope and linear_constant of the line equation that 
        connects point_A to point_B
        """
        if self.point_B.x - self.point_A.x == 0: # line is parallel in the y axis
            return None, None
        else:
            slope = (self.point_B.y - self.point_A.y) /\
                    (self.point_B.x - self.point_A.x)
            linear_constant = -slope*self.point_A.x + self.point_A.y
            return (slope, linear_constant)
        

class Plane():

    def __init__(self):
        pass

class Triangle():

    def __init__(self):
        pass

