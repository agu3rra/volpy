# Publish by:
# python3 setup.py sdist bdist_wheel
# twine upload dist/*

from setuptools import setup, find_packages

setup(
    name='volpy',
    version='0.1.2dev',
    packages=find_packages(),
    install_requires=['numpy',
                      'pandas',
                      'utm',
                      'sympy',
                      'plotly',],

    package_data={
        'volpy': ['sample_data/*.csv', 'sample_data/*.gpx', 'sample_data/*.txt', ],
    },

    author='Andre Guerra',
    author_email='agu3rra@gmail.com',
    description='volpy: Volume calculations in Python',
    long_description='Calculate volumes out of a Digital Elevation Model (DEM) represented by Triangulated Irregular Network',
    url='https://github.com/agu3rra/volpy/',
    license='GPL',
    keywords='gps volume terrain survey'
)
