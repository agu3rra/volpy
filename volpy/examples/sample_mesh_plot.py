import sys
sys.path.append('../bin')
from survey import Survey

SAMPLE = '../sample_data/survey_ibema_faxinal_Cartesian.csv'
survey = Survey(SAMPLE, 'SAMPLE')

from plots import SurveyPlot
sp = SurveyPlot(survey)
sp.mesh_plot()
