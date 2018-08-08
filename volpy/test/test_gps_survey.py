import unittest
import sys
import os
sys.path.append('../lib')

from gps_survey import GpsDevice
from gps_survey import GpsSurvey

class GpsSurveyTestCase(unittest.TestCase):


    def test_ImportCleanData(self):
        SAMPLE_DATA = '../sample_data/survey_ibema_faxinal.gpx'
        sample_survey = GpsSurvey("Sample initialization", SAMPLE_DATA)
        self.assertEqual(sample_survey.data.shape[0], 155)

    def test_ImportDirtyData(self):
        SAMPLE_DATA = '../sample_data/survey_ibema_faxinal_dirty.gpx'
        sample_survey = GpsSurvey("Sample initialization", SAMPLE_DATA)
        # As we know only 152 points are valid in the dirty sample
        self.assertEqual(sample_survey.data.shape[0], 152)

if __name__ == '__main__':
    unittest.main()
