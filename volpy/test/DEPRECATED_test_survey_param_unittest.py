import pandas as pd
import unittest
import sys
sys.path.append('../lib')

from survey import Survey
sample_directory = '../sample_data/'

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

# Define parameterized testing data
test_case_data_success = \
{
    "successful_file_import": 
        [('survey_ibema_faxinal.gpx', 155, 880.68),
         ('survey_ibema_faxinal_corrupt.gpx', 152, 878.91),
         ('survey_ibema_faxinal.csv', 155, 880.68)
        ]
}

test_case_data_error = \
{
    "import_type_error":
        [('invalid_source_format.bla')],
    "import_value_error":
        [('survey_ibema_faxinal_unexpectedLat.gpx'),
         ('survey_ibema_faxinal_unexpectedTrackPoint.gpx'),
         ('survey_ibema_faxinal_invalidColumn.csv'),
         ('survey_ibema_faxinal_noHeader.csv'),
         ('survey_ibema_faxinal_WrongValue.csv')
        ]
}

# Testing templates
def template_successful_import(*args):
    def foo(self):
        self.assert_successful_import(*args)
    return foo

# Test class
class SurveyImportTest(unittest.TestCase):

    # Custom assertions
    def assert_successful_import(self, source, entries, expected):
        survey = Survey(sample_directory + source, 'Test survey')
        self.assertEqual(survey.data.shape[0], entries)
        self.assertEqual(survey.data.iloc[3,6], expected)
        self.assertTrue(verify_survey_dtypes(survey))

# Dynamically creating tests
for behaviour, test_cases in test_case_data_success.items():
    for case_data in test_cases:
        source, entries, value = case_data
        test_name = "test_{0}_{1}_{2}_{3}".format(behaviour,
                                              source,
                                              entries,
                                              value)
        test_case = template_successful_import(*case_data)
        setattr(SurveyImportTest, test_name, test_case)