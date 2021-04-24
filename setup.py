from setuptools import setup, find_packages

setup(
    name='volpy',
    version='21.4.1',
    packages=find_packages(),
    install_requires=['numpy==1.20.0',
                      'scipy==1.3.1',
                      'pandas==1.2.4',
                      'utm==0.7.0',
                      'sympy==1.6.2',
                      'plotly==4.14.3',],

    package_data={
        'volpy': ['sample_data/survey_ibema_faxinal_Cartesian.csv', ],
    },

    author='Andre Guerra',
    author_email='agu3rra@me.com',
    description='volpy: Volume calculations in Python',
    long_description='Calculate volumes out of a Digital Elevation Model (DEM) represented by Triangulated Irregular Network',
    url='https://github.com/agu3rra/volpy/',
    license='MIT',
    keywords='gps volume terrain survey'
)
