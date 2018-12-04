from setuptools import setup, find_packages

setup(
    name='volpy',
    version='0.1.8dev',
    packages=find_packages(),
    install_requires=['numpy',
                      'scipy',
                      'pandas',
                      'utm',
                      'sympy',
                      'plotly',],

    package_data={
        'volpy': ['sample_data/survey_ibema_faxinal_Cartesian.csv', ],
    },

    author='Andre Guerra',
    author_email='agu3rra@gmail.com',
    description='volpy: Volume calculations in Python',
    long_description='Calculate volumes out of a Digital Elevation Model (DEM) represented by Triangulated Irregular Network',
    url='https://github.com/agu3rra/volpy/',
    license='GPL',
    keywords='gps volume terrain survey'
)
