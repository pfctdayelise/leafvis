#! /usr/bin/env python

""" leafvis package configuration """

from setuptools import setup, find_packages

DISTNAME = 'leafvis'
DESCRIPTION = 'Image Visualization (using Leaflet.js)'
LONG_DESCRIPTION = """
A python based layer visualization library that leverages off the excellent 
map visualization tool, leaflet.js.
"""
MAINTAINER = 'Nathan Faggian'
MAINTAINER_EMAIL = 'nathan.faggian@gmail.com'
URL = 'https://github.com/nfaggian/leafvis'
LICENSE = 'Apache License (2.0)'
DOWNLOAD_URL = 'https://github.com/nfaggian/leafvis.git'

VERSION = imreg.__version__

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Scientific/Engineering'
    ]

setup(
    name=DISTNAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    license=LICENSE,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    package_data={},
    install_requires=[
       'flask',
       'numpy',
       'joblib',
       'pyproj',
       'pyresample'
       ],
    zip_safe=False
    )
