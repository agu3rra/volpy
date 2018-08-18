import pytest
import pandas as pd
import sys
sys.path.append('../lib')

from survey import Survey
sample_directory = '../sample_data/'

test_cases = (
    ('source', 'entries', 'expected'),
        [
            ('survey_ibema_faxinal.gpx', 155, 880.68),
            ('survey_ibema_faxinal_corrupt.gpx', 152, 878.91),
            ('survey_ibema_faxinal.csv', 155, 880.68),
        ]
)

def verify_survey_dtypes(survey):
    """
    Verifies if dataframe is formed of desired data types

    Arguments:
    survey: an instance of the Survey class.

    Returns True on match and False otherwise
    """
    index_type = type(survey.data.index)
    actual_column_types = survey.data.dtypes

    if index_type != pd.core.indexes.datetimes.DatetimeIndex:
        return False

    for column in survey.data.columns:
        expected_type = survey._column_names[column]
        if expected_type != actual_column_types[column]:
            return False

    return True

@pytest.mark.parametrize(*test_cases)
def test_successful_import(source, entries, expected):
        survey = Survey(sample_directory + source, 'Test survey')
        assert survey.data.shape[0] == entries
        assert survey.data.iloc[3,6] == expected
        assert verify_survey_dtypes(survey) == True