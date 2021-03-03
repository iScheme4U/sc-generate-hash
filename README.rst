.. image:: https://badge.fury.io/py/sc-generate-hash.svg
    :target: https://badge.fury.io/py/sc-generate-hash
.. image:: https://img.shields.io/pypi/pyversions/sc-generate-hash
    :alt: PyPI - Python Version

A simple utilities for generating hash values from files
========================================================

This project provides a simple utilities for generating hash values from files.


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-generate-hash

Configuration
-------------

First, make sure /var/opt/sc directory exists, if not create this directory and make sure current user has the right
to create files in this directory.

You can copy `default.yml <https://github.com/Scott-Lau/sc-generate-hash/blob/master/sc_hash/tests/sample_config/default.yml>`_
to /var/opt/sc/.sc-generate-hash/production.yml to initialize the production configuration.

The default configuration file looks like this::

    dev:
      # whether this program is running is development mode
      dev_mode: False
    # directories to be scanned for jars
    scan_libs:
      - /tmp/libs
      - /tmp/libs2


Dependencies
------------

* `sc-utilities <https://github.com/Scott-Lau/sc-utilities>`_ >= 0.0.2
* `sc-config <https://github.com/Scott-Lau/sc-config>`_ >= 0.0.3

Changes
-------

Version 0.0.1
    * Initial version

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
