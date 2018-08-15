import plotly
import plotly.offline as po
import plotly.graph_objs as go

class Plots():
    """Groups different plot types on  data"""

    def __init__(self, x, y, xaxis, yaxis, title):
        """
        Initializer

        Arguments:
        x: pandas Series for the x axis data
        y: pandas Series for the y axis data
        xaxis: x axis label
        yaxis: y axis label
        title: the title of the plot
        """
        self.x = x
        self.y = y
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.title = title

    def line(self):
        """Plots the elevation along the survey path."""
        layout = go.Layout(
            title=self.title,
            xaxis=dict(title=self.xaxis),
            yaxis=dict(title=self.yaxis),
            autosize=True)
        trace = go.Scatter(
            x = self.x,
            y = self.y,
            mode = 'lines+markers',
            name = self.title
        )
        po.plot({"data": [trace], "layout": layout})
