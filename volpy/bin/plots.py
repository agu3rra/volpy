import numpy as np
from sympy import symbols
import plotly
import plotly.offline as po
import plotly.graph_objs as go
from plotly import tools

from geometry import TriangularMesh
from coordinates import CartesianCoordinate
from geometry import Triangle


class SurveyPlot():
    """Groups different plot types on  data"""

    def __init__(self, survey):
        """
        Initializer

        Arguments:
        survey: an instance of Survey
        """
        self.survey = survey

    def scatter3d(self):
        layout = go.Layout(title='Terrain Point Cloud', autosize=True)
        trace = go.Scatter3d(x=self.survey.data.x,
                             y=self.survey.data.y,
                             z=self.survey.data.z,
                             mode='markers',
                             marker=dict(size=4,
                                         line=dict(color='#fff3ff',
                                                   width=0.5),
                                         opacity=0.8),
                             connectgaps=False,
                             name='Terrain Point Cloud')

        figure = go.Figure(data=[trace], layout=layout)
        return po.plot(figure, filename='3d_view.html')

    def contour(self):
        layout = go.Layout(title='Terrain Contour', autosize=True)
        trace = go.Contour(x=self.survey.data.x,
                           y=self.survey.data.y,
                           z=self.survey.data.z)
        figure = go.Figure(data=[trace], layout=layout)
        return po.plot(figure, filename='Contour.html')

    def scatter(self, x, y, name):
        return go.Scatter(
            x=x,
            y=y,
            name=name,
            mode='markers',
            marker=dict(
                size=4,
                opacity=0.8,
                # color=color,
                # colorscale='Viridis'
            ),
            connectgaps=False)

    def histogram(self, x, name):
        return go.Histogram(x=x,
                            name=name,
                            histfunc='count',
                            marker=dict(color='#ffb800'))

    def generate_subplots(self):
        figure = tools.make_subplots(rows=2,
                                     cols=2,
                                     subplot_titles=('Survey points collected',
                                                     'Top View: XY',
                                                     'Elevation(m): XZ',
                                                     'Elevation(m): YZ'))
        figure['layout'].update(title='Survey plots')
        trace_histogram = self.histogram(
            self.survey.data.z, 'Elevation Histogram')
        trace_top = self.scatter(self.survey.data.x,
                                 self.survey.data.y,
                                 'Top View')
        trace_xz = self.scatter(self.survey.data.x,
                                self.survey.data.z,
                                'XZ')
        trace_yz = self.scatter(self.survey.data.y,
                                self.survey.data.z,
                                'YZ')
        figure.append_trace(trace_histogram, 1, 1)
        figure.append_trace(trace_top, 1, 2)
        figure.append_trace(trace_xz, 2, 1)
        figure.append_trace(trace_yz, 2, 2)
        return po.plot(figure, filename='survey_subplots.html')

    def mesh_plot(self):
        """Plots a top view of the triangular mesh for the survey"""

        # Adjust for 3 different colors
        colors = {1: 'red',
                  2: 'yellow',
                  3: 'blue'}
        current_color = 1

        triangular_mesh = TriangularMesh(self.survey.data)
        data_amount = len(triangular_mesh.data)
        data = []
        for i in range(data_amount):
            A = triangular_mesh.point_cloud.iloc[triangular_mesh.data[i][0]]
            B = triangular_mesh.point_cloud.iloc[triangular_mesh.data[i][1]]
            C = triangular_mesh.point_cloud.iloc[triangular_mesh.data[i][2]]
            trace = go.Scatter(
                x=[A['x'], B['x'], C['x']],
                y=[A['y'], B['y'], C['y']],
                mode='markers',
                marker=dict(
                    size=4,
                    opacity=0.3,
                    color=colors[current_color]),
                connectgaps=False,
                fill='toself',
                showlegend=False)
            data.append(trace)

            # Color control
            current_color += 1
            if (current_color > 3):
                current_color = 1

        figure = go.Figure(data=data)
        return po.plot(figure, filename='mesh.html')
