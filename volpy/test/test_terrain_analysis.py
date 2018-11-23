import pytest
import sys
sys.path.append('../')

from coordinates import CoordinateSystem
from survey import Survey
from terrain_analysis import TerrainAnalysis

def test_cut_fill_01():
    source = '../sample_data/survey_delaunay_Cartesian.csv'
    survey = Survey(source,
                    'sample',
                    coordinate_system=CoordinateSystem.CARTESIAN)
    analysis = TerrainAnalysis(survey, swell=1.4)
    cut, fill_raw, fill_swell = analysis.get_volumes(1.0)
    # Find in literature if soil swell factor (from portuguese: empolamento) is
    # about less cut terrain being required (because it swells once it is out.
    # I believe because if was highly compacted)
    pass