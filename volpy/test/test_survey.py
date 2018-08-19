# python -m pytest test_survey.py
# python -m pytest --verbose
import pytest
import pandas as pd
import sys
sys.path.append('../lib')

from survey import Survey
from coordinates import CoordinateSystem
sample_directory = '../sample_data/'

# Successful import tests
test_cases = (('source', 'entries', 'expected', 'coordinate_system'),
[
('survey_ibema_faxinal.gpx',155, 880.68, CoordinateSystem.GEOGRAPHIC),
('survey_ibema_faxinal_Geographic.csv', 155, 880.68, CoordinateSystem.GEOGRAPHIC),
('survey_ibema_faxinal_UTM.csv', 155, 880.68, CoordinateSystem.UTM),
('survey_ibema_faxinal_Cartesian.csv', 155, 880.68, CoordinateSystem.CARTESIAN),
('survey_ibema_faxinal_Geographic.txt', 155, 880.68, CoordinateSystem.GEOGRAPHIC),
('survey_ibema_faxinal_UTM.txt', 155, 880.68, CoordinateSystem.UTM),
('survey_ibema_faxinal_Cartesian.txt', 155, 880.68, CoordinateSystem.CARTESIAN),
])

def verify_survey_dtypes(survey):
    """
    Verifies if dataframe is formed of desired data types

    Arguments:
    survey: an instance of the Survey class.

    Returns True on match and False otherwise
    """
    actual_column_types = survey.data.dtypes
    for column in survey.data.columns:
        if actual_column_types[column] != 'float64':
            return False
    return True

@pytest.mark.parametrize(*test_cases)
def test_successful_import(source, entries, expected, coordinate_system):
        survey = Survey(sample_directory + source,
                        'Test survey',
                        coordinate_system)
        assert survey.data.shape[0] == entries
        assert survey.data.shape[1] == 4 # x,y,z,elevation columns
        assert survey.data.iloc[3,3] == expected # elevation info
        assert verify_survey_dtypes(survey) == True

# Expected import error tests
test_cases = (('source', 'error_type'),
        [
            ('invalid_source_format.bla', TypeError),
            ('survey_ibema_faxinal_corrupt.gpx', ValueError),
            ('survey_ibema_faxinal_unexpectedLat.gpx', ValueError),
            ('survey_ibema_faxinal_unexpectedTrackPoint.gpx', ValueError),
            ('survey_ibema_faxinal_Cartesian_invalid_column.csv', ValueError),
            ('survey_ibema_faxinal_Cartesian_no_header.csv', ValueError),
            ('survey_ibema_faxinal_Cartesian_wrong_entry.csv', ValueError),
            ('survey_ibema_faxinal_Cartesian_invalid_column.txt', ValueError),
            ('survey_ibema_faxinal_Cartesian_no_header.txt', ValueError),
            ('survey_ibema_faxinal_Cartesian_wrong_entry.txt', ValueError),
            ('survey_ibema_faxinal_Geographic_invalid_column.csv', ValueError),
            ('survey_ibema_faxinal_Geographic_no_header.csv', ValueError),
            ('survey_ibema_faxinal_Geographic_wrong_entry.csv', ValueError),
            ('survey_ibema_faxinal_Geographic_invalid_column.txt', ValueError),
            ('survey_ibema_faxinal_Geographic_no_header.txt', ValueError),
            ('survey_ibema_faxinal_Geographic_wrong_entry.txt', ValueError),
            ('survey_ibema_faxinal_UTM_invalid_column.csv', ValueError),
            ('survey_ibema_faxinal_UTM_no_header.csv', ValueError),
            ('survey_ibema_faxinal_UTM_wrong_entry.csv', ValueError),
            ('survey_ibema_faxinal_UTM_invalid_column.txt', ValueError),
            ('survey_ibema_faxinal_UTM_no_header.txt', ValueError),
            ('survey_ibema_faxinal_UTM_wrong_entry.txt', ValueError),
        ])

@pytest.mark.parametrize(*test_cases)
def test_import_error(source, error_type):
        source = sample_directory + source
        with pytest.raises(error_type):
            _ = Survey(source, 'sample')