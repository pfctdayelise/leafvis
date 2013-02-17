Leaflet based visualization framework
=====================================

This package makes it possible to easily visualize gridded meteorological data, represented as numpy arrays, using the *excellent* javascript visualization library leaflet.

References:
-----------

     Vladimir Agafonkin, http://leafletjs.com/index.html. 


Maintainers
-----------

   - Nathan Faggian

Testing
-------

[![Build Status](https://travis-ci.org/nfaggian/leafvis.png?branch=master)](https://travis-ci.org/nfaggian/leafvis)

Dependencies
------------

The required dependencies to build the software are:

  - python
  - numpy
  - scipy
  - flask
  - pyproj
  - matplotlib
  - pyresample
  - py.test

Install
-------

This packages uses distutils, which is the default way of installing python modules. To install in your home directory, use:

    python setup.py install --home

To install for all users on Unix/Linux:

    python setup.py build
    sudo python setup.py install

Examples
--------

Refer to ``/notebooks/example.ipynb``.

Development
-----------

Follow: Fork + Pull Model:

    http://help.github.com/send-pull-requests/