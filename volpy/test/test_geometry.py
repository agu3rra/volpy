import pytest
import sys
sys.path.append('../bin')
from coordinates import CartesianCoordinate
from geometry import Line2D


"""
Test Line2D correctly represents a line. Cases below were calculated manually.
"""
test_cases = (('point_A', 'point_B', 'slope', 'linear_constant'),
[
(CartesianCoordinate(3,5,8), CartesianCoordinate(4,2,4), -3.0, 14.0),
(CartesianCoordinate(3,5,8), CartesianCoordinate(3,2,4), 0.0, 0.0),
(CartesianCoordinate(19.34,3.12,8), CartesianCoordinate(0.5,-8.12,4), 0.597, 0.-8.418),
]
)

@pytest.mark.parametrize(*test_cases)
def test_2dLine(point_A, point_B, slope, linear_constant):
    line = Line2D(point_A, point_B)
    calculated_slope, calculated_linear_constant = line.get_parameters()
    assert calculated_slope == pytest.approx(slope, 0.002)
    assert calculated_linear_constant == pytest.approx(linear_constant, 0.002)