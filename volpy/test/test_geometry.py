import pytest
import numpy as np
import sys
sys.path.append('../bin')

from coordinates import CartesianCoordinate
from geometry import Line2D


"""
Test Line2D correctly represents a line. Cases below were calculated manually.
"""
test_cases = (('point_A', 'point_B', 'slope', 'linear_constant'),
[
    (CartesianCoordinate(3, 5, 8),
     CartesianCoordinate(4, 2, 4),
     -3.0,
     14.0),

    (CartesianCoordinate(3, 5, 8),
     CartesianCoordinate(3, 2, 4),
     0.0,
     0.0),

    (CartesianCoordinate(19.34, 3.12, 8),
     CartesianCoordinate(0.5, -8.12, 4),
     0.597,
     -8.418),
])

@pytest.mark.parametrize(*test_cases)
def test_2dLine(point_A, point_B, slope, linear_constant):
    line = Line2D(point_A, point_B)
    calculated_slope, calculated_linear_constant = line.get_parameters()
    assert calculated_slope == pytest.approx(slope, 0.002)
    assert calculated_linear_constant == pytest.approx(linear_constant, 0.002)

"""
Test the subtraction of Cartesian Coordinates
"""
test_cases = (('point_A', 'point_B', 'expected'),
[
    (CartesianCoordinate(1, 5, 8),
     CartesianCoordinate(6, 2, 10),
     np.array([5, -3, 2])),

    (CartesianCoordinate(8.5, -13, 5),
     CartesianCoordinate(1.72, 70.5, 10.8),
     np.array([-6.78, 83.5, 5.8])),
])

@pytest.mark.parametrize(*test_cases)
def test_point_subtraction(point_A, point_B, expected):
    vector_AB = point_B - point_A
    assert np.allclose(vector_AB, expected)


"""
Test plane equation is correctly defined.
"""

"""
Test volume of a triangle is calculated as expected.
"""