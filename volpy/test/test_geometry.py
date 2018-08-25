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
(CartesianCoordinate(3,5,8), CartesianCoordinate(4,2,4), 34, 13),
(),
(),
(),
]
)

@pytest.mark.parametrize(*test_cases)
def test_2dLine(point_A, point_B, slope, linear_constant):
    line = Line2D(point_A, point_B)
    calculated_slope, calculated_linear_constant = line.get_parameters()
    assert calculated_slope == slope
    assert calculated_linear_constant == linear_constant