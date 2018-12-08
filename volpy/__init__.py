from pkg_resources import resource_filename
from .coordinates import CoordinateSystem
from .survey import Survey as load_survey
from .geometry import TriangularMesh as terrain_mesh
from .plots import SurveyPlot as terrain_plots

import volpy as vp
sample = resource_filename(__name__, 'sample_data/survey_ibema_faxinal_Cartesian.csv')

def demo():
    """
    A quick demo of this package. It loads a dataset available internally,
    displays information about it and related graphs: 3D Scatter, Contour,
    Histogram and 2D Scatter and finally the Volume Curves.
    """
    print("Loading sample survey data...")
    survey = load_survey(sample,
        'Ibema Faxinal')
    if survey is not None:
        print('Sample survey data loaded successfully.')
        print("---")
        print("Sample survey information:")
        print("Maximum elevation: {:.2f} meters.".format(
            survey.data['elevation'].max()))
        print("Elevation delta: {:.2f} meters.".format(
            survey.data['elevation'].max() - survey.data['elevation'].min()))
        print("Survey data count: {} points.".format(
            survey.data['elevation'].count()))
        print("---")
        print("Generating survey plots...")
        """"
        plots = terrain_plots(survey)
        plots.scatter3d()
        plots.contour()
        plots.profile()
        plots.mesh_plot()
        print('---')
        print('Calculating total terrain volume...')
        """
        mesh = terrain_mesh(survey.data)
        print("Generating volume curves...")
        curves = mesh.get_volume_curves()
        print(curves)
        mesh.plot_curves(curves)
        """"
        volume = mesh.get_volume()
        print("Total volume: {:.2f} cubic meters".format(volume))
        """
    else:
        print('Error while loading sample survey data.')
