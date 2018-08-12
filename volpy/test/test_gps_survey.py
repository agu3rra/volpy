import pytest
import sys
sys.path.append('../lib')
from gps_survey import GpsDevice
from gps_survey import GpsSurvey

def test_ImportCleanData():
    SAMPLE_DATA = '../sample_data/survey_ibema_faxinal.gpx'
    sample_survey = GpsSurvey("Sample initialization", SAMPLE_DATA)
    assert sample_survey.data.shape[0] == 155

def test_ImportDirtyData():
    SAMPLE_DATA = '../sample_data/survey_ibema_faxinal_dirty.gpx'
    sample_survey = GpsSurvey("Sample initialization", SAMPLE_DATA)
    # As we know only 152 points are valid in the dirty sample
    assert sample_survey.data.shape[0] == 152