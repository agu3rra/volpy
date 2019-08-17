from setuptools import setup, find_packages

setup(
    name='volpy',
    version='19.8.1',
    packages=find_packages(),
    install_requires=['numpy==1.17.0',
                      'scipy==1.3.1',
                      'pandas==0.25.0',
                      'utm==0.5.0',
                      'sympy==1.4',
                      'plotly==4.1.0',],

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
