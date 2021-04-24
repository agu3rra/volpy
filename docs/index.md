# Volume Calculations for Digital Elevation Models in Python (**volpy**)

The purpose of this Python project is to provide the means of calculating volumes out of a Digital Elevation Model ([DEM](https://en.wikipedia.org/wiki/Digital_elevation_model)) represented by Triangulated Irregular Network ([TIN](https://en.wikipedia.org/wiki/Triangulated_irregular_network)).

Its main goal is to provide sufficiently accurate volume estimates out of terrain surveys for an area of construction work where ground leveling is required prior to the actual construction activity.

## Preview

<iframe width=700, height=500 frameBorder=0 src="img/Contour.html"></iframe>

<iframe width=700, height=500 frameBorder=0 src="img/3d_view.html"></iframe>

<iframe width=700, height=500 frameBorder=0 src="img/profile.html"></iframe>

<iframe width=700, height=500 frameBorder=0 src="img/volume_curves.html"></iframe>

## Installation
```bash
$ pip install volpy
```

## Quick demo

```Python
import volpy as vp
vp.demo()
```

## Simple use case

```Python
import volpy as vp
survey = vp.load_survey('survey_data.csv')
mesh = vp.terrain_mesh(survey.data)
survey.get_bounds()
> 'x=250.13, y=402.14, z=11.54'
# Survey plots
plots = vp.terrain_plots(survey)
plots.scatter3d()
plots.contour()
plots.profile()
plots.mesh_plot()
vol_curves = mesh.get_volume_curves(step=1.0)
mesh.plot_curves(vol_curves)

# Just a volume from the mesh
mesh.get_volume()
```

By default, volpy applies its calculations on a [Cartesian Coordinate System](https://en.wikipedia.org/wiki/Cartesian_coordinate_system). If you are working with survey data obtained from a [GPS](https://en.wikipedia.org/wiki/Global_Positioning_System), its points are likely represented in a [Geographic Coordinate System](https://en.wikipedia.org/wiki/Geographic_coordinate_system). In order to convert it, use the following modifier when loading the data.

```Python
survey = vp.load_survey(
    'survey_data.csv',
    coordinates=vp.CoordinateSystem.GEOGRAPHIC
)
```
