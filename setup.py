#! /usr/bin/env python

""" imreg package configuration """
import numpy
import imreg

from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

DISTNAME = 'imreg'
DESCRIPTION = 'Image registration toolkit'
LONG_DESCRIPTION = """
"imreg" is an image registration package for python that makes it easy to
automatically align image data.
"""
MAINTAINER = 'Nathan Faggian, Riaan Van Den Dool, Stefan Van Der Walt'
MAINTAINER_EMAIL = 'nathan.faggian@gmail.com'
URL = 'pyimreg.github.com'
LICENSE = 'Apache License (2.0)'
DOWNLOAD_URL = ''

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
    cmdclass={
            'build_ext': build_ext
        },
    ext_modules=[Extension("imreg.interpolation", ["imreg/_interpolation.pyx"], )],
    include_dirs=[numpy.get_include(), ],
    package_data={},
    install_requires=[
       'numpy',
       'scipy'
       ],
    zip_safe=False
    )
