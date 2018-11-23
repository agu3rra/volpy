import pytest
import numpy as np
from sympy import symbols

import sys
sys.path.append('../')

from coordinates import CartesianCoordinate
from coordinates import CoordinateSystem
from geometry import Line2D
from geometry import Triangle
from geometry import TriangularMesh
from survey import Survey

"""
Test Line2D correctly represents a line. Cases below were calculated manually.
"""
test_cases = (('point_A', 'point_B', 'input_x', 'output_y'),
[
    (CartesianCoordinate(3, 5, 8),
     CartesianCoordinate(4, 2, 4),
     9.0,
     -13), # Assert that f(9)=-13 for the line AB

    (CartesianCoordinate(3, 5, 8),
     CartesianCoordinate(3, 2, 4),
     163.4,
     None),

    (CartesianCoordinate(19.34, 3.12, 8),
     CartesianCoordinate(0.5, -8.12, 4),
     18,
     2.328),
])

@pytest.mark.parametrize(*test_cases)
def test_2dLine(point_A, point_B, input_x, output_y):
    line = Line2D(point_A, point_B)
    line_equation = line.get_line_equation()
    if line_equation is None:
        output_y_calculated = None
        assert output_y == output_y_calculated
    else:
        x = symbols('x')
        output_y_calculated = float(line_equation.subs(x, input_x))
        assert output_y == pytest.approx(output_y_calculated, abs=0.01)

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
test_cases = (
    ('point_A', 'point_B', 'point_C', 'input_y', 'input_x', 'output_z'),
    [
    (CartesianCoordinate(3, 0, 8),
    CartesianCoordinate(5, 9, 1),
    CartesianCoordinate(10, 4, 7),
    32,
    18,
    -14.164)
    ]
)

@pytest.mark.parametrize(*test_cases)
def test_plane_equation(point_A, point_B, point_C, input_y, input_x, output_z):
    triangle = Triangle(point_A, point_B, point_C)
    plane = triangle.get_plane_equation()
    x, y = symbols('x y')
    output_z_calculated = float(plane.subs([(x, input_x), (y, input_y)]))
    assert output_z_calculated == pytest.approx(output_z, abs=0.01)

"""
Test volume of a triangle is calculated as expected.
"""
test_cases = (
    ('point_A', 'point_B', 'point_C', 'expected_volume'),
    [
        (CartesianCoordinate(3, 0, 8),
         CartesianCoordinate(5, 9, 1),
         CartesianCoordinate(10, 4, 7),
         146.67),

        (CartesianCoordinate(5, 9, 1),
         CartesianCoordinate(3, 0, 8),
         CartesianCoordinate(10, 4, 7),
         146.67),

        (CartesianCoordinate(10, 4, 7),
         CartesianCoordinate(3, 0, 8),
         CartesianCoordinate(5, 9, 1),
         146.67),

        # Create test case for a prism.
         (CartesianCoordinate(5, 0, 20),
         CartesianCoordinate(0, 10, 20),
         CartesianCoordinate(0, 0, 20),
         500.00),

         (CartesianCoordinate(15, 10, 20),
         CartesianCoordinate(5, 5, 20),
         CartesianCoordinate(10,15, 20),
         750.00)
         
    ]
)

@pytest.mark.parametrize(*test_cases)
def test_volume_calculation(point_A, point_B, point_C, expected_volume):
    triangle = Triangle(point_A, point_B, point_C)
    volume = triangle.get_volume()
    assert volume == pytest.approx(expected_volume, abs=0.05)


"""Test sorting of Cartesian Coordinates as a function of their x coordinate"""
test_cases = (
    ('point_A', 'point_B'),
    [
        (CartesianCoordinate(8, 12, 5), CartesianCoordinate(10, 9, 2))
    ]
)

@pytest.mark.parametrize(*test_cases)
def test_cartesian_sorting(point_A, point_B):
    array = [point_B, point_A]
    array.sort()
    print(array)
    assert array[0] == point_A
    assert array[1] == point_B

"""Test Mesh Volume"""
def test_mesh_volume():
    source = '../sample_data/survey_delaunay_Cartesian.csv'
    survey = Survey(source,
                    'sample',
                    coordinate_system=CoordinateSystem.CARTESIAN)
    mesh = TriangularMesh(survey.data)
    assert mesh.get_volume() == pytest.approx(168.0, rel=0.01)
