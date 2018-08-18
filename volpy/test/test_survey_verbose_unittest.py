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

class GpxTestCase(unittest.TestCase):

    def test_ImportUnknownExtension(self):
        source_file = sample_directory + 'invalid_source_format.bla'
        with self.assertRaises(TypeError):
            _ = Survey(source_file, 'Dummy survey for test')

    def test_ImportFromGPX(self):
        source_file = sample_directory + 'survey_ibema_faxinal.gpx'
        survey = Survey(source_file, 'Survey Ibema Faxinal')
        self.assertEqual(survey.data.shape[0], 155)
        self.assertEqual(survey.data.iloc[3,6], 880.68)
        self.assertTrue(verify_survey_dtypes(survey))

    def test_ImportFromGPX_CorruptFile(self):
        source_file = sample_directory + 'survey_ibema_faxinal_corrupt.gpx'
        survey = Survey(source_file, 'Survey Ibema Faxinal - Dirty Sample')
        self.assertEqual(survey.data.shape[0], 152)
        self.assertEqual(survey.data.iloc[3,6], 878.91)
        self.assertTrue(verify_survey_dtypes(survey))

    def test_ImportUnexpectedGpxFormat(self):
        source_file = sample_directory + 'survey_ibema_faxinal_unexpectedLat.gpx'
        with self.assertRaises(ValueError):
            _ = Survey(source_file, 'sample')

    def test_ImportUnexpectedGpxFormat2(self):
        source_file = sample_directory + 'survey_ibema_faxinal_unexpectedTrackPoint.gpx'
        with self.assertRaises(ValueError):
            _ = Survey(source_file, 'sample')

class CsvTestCase(unittest.TestCase):

    def test_ImportFromCsv(self):
        source_file = sample_directory + 'survey_ibema_faxinal.csv'
        survey = Survey(source_file, 'sample')
        self.assertEqual(survey.data.shape[0], 155)
        self.assertEqual(survey.data.iloc[3,6], 880.68)
        self.assertTrue(verify_survey_dtypes(survey))

    def test_ImportFromCsvUnknownColumnNames(self):
        source_file = sample_directory + 'survey_ibema_faxinal_invalidColumn.csv'
        with self.assertRaises(ValueError):
            _ = Survey(source_file, 'sample')

    def test_ImportFromCsvNoHeader(self):
        source_file = sample_directory + 'survey_ibema_faxinal_noHeader.csv'
        with self.assertRaises(ValueError):
            _ = Survey(source_file, 'sample')

    def test_ImportFromCsvInvalidDataType(self):
        source_file = sample_directory + 'survey_ibema_faxinal_WrongValue.csv'
        with self.assertRaises(ValueError):
            _ = Survey(source_file, 'sample')

    def test_ImportFromXlsx(self):
        pass

    def test_ImportFromXls(self):
        pass


if __name__ == '__main__':
    unittest.main()
