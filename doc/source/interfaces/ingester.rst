.. BAIP Loader Interface: Ingester

.. toctree::
    :maxdepth: 2

.. _ingester:

Ingester
========

The BAIP Loader ``ingest`` context is responsible for sourcing translated
CSIRO Metadata JSON files and ingest into the
`data.gov.au <http://data.gov.au/>`_ endpoint.

Ingester Workflow
-----------------

.. todo::

    Ingester workflow

JSON File Source
^^^^^^^^^^^^^^^^
Typical organisation of the generated files is as follows::

    $ ls -1 /var/tmp/baip-loader/
    457ED79A-C6DF-4AAF-A480-00926E48CAA8.json
    6151C409-0CAF-4727-9F57-00F6B71A58FB.json
    6968B11F-9912-42CA-8536-00CDE75E75D9.json
    781A8B81-93B8-4CDE-9B56-00291D7543EA.json
    DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json

.. _ingester_configuration:

Configuration
-------------

JSON File Source Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^
Mapped JSON files are placed under the ``inbound_dir`` configuration
item::

    inbound_dir: /var/tmp/baip-loader

.. note::

    The ``inbound_dir`` configuration setting is shared with the
    ``dump`` context and essentially is a staging area for CKAN JSON files.

``baip-loader ingest`` Usage
----------------------------

::

    $ baip-loader ingest --help
    usage: baip-loader ingest [-h] [-i INFILE]

    optional arguments:
        -h, --help            show this help message and exit
        -i INFILE, --input-file INFILE
                              Source JSON filename and attempt ingest

