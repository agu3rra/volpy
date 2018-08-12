import unittest
import sys
sys.path.append('../lib')
from survey import Survey

class SurveyTestCase(unittest.TestCase):

    def test_ImportUnknownExtension(self):
        source_file = '../sample_data/invalid_source_format.bla'
        with self.assertRaises(TypeError):
            survey = Survey(source_file, 'Dummy survey for test')

    def test_ImportFromGPX(self):
        source_file = '../sample_data/survey_ibema_faxinal.gpx'
        survey = Survey(source_file, 'Survey Ibema Faxinal')
        self.assertEqual(survey.data.shape[0], 155)
        self.assertEqual(survey.data.iloc[3,6], 880.68)

    def test_ImportFromGPX_CorruptFile(self):
        source_file = '../sample_data/survey_ibema_faxinal_corrupt.gpx'
        survey = Survey(source_file, 'Survey Ibema Faxinal - Dirty Sample')
        self.assertEqual(survey.data.shape[0], 152)
        self.assertEqual(survey.data.iloc[3,6], 878.91)

    def test_ImportUnexpectedGpxFormat(self):
        source_file = '../sample_data/survey_ibema_faxinal_unexpectedLat.gpx'
        with self.assertRaises(IOError):
            survey = Survey(source_file, 'sample')
        source_file = '../sample_data/survey_ibema_faxinal_unexpectedTrackPoint.gpx'
        with self.assertRaises(IOError):
            survey = Survey(source_file, 'sample')

    def test_ImportFromCSV(self):
        pass

    def test_ImportFromXlsx(self):
        pass

    def test_ImportFromXls(self):
        pass




if __name__ == '__main__':
    unittest.main()
