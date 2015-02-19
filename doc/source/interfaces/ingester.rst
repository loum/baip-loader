.. BAIP Loader Interface: Ingester

.. toctree::
    :maxdepth: 2

.. _ingester:

Ingester
========

The BAIP Loader ``ingest`` context is responsible for sourcing translated
CSIRO Metadata JSON files and ingest into the
`data.gov.au <http://data.gov.au/>`_ endpoint.

Programmatically, the ingest process closely follows the
`CKAN guide for making an API request <http://docs.ckan.org/en/latest/api/index.html?highlight=importer#making-an-api-request>`_.  In brief, we use
the :mod:`urllib2` module to create a HTTP request.  The request header
is modified accordingly to authenticate connectivity and satisfy the
API's validation requirements.  The required request/validation
parameters will be detailed here.

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

CKAN Ingest Endpoint
^^^^^^^^^^^^^^^^^^^^

``baip-loader ingest`` context takes its runtime parameters from the
``/etc/baip/conf/loader.conf`` file.  The CKAN target endpoint
can be configured under the ``[ckan]`` section.  The supported settings
form the general structure of the URL in the format::

    scheme://netloc/path

For example, the following configuration is assocated with the URL
``http://test.ddg.lws.links.com.au/api/action/package_create``::

    [ckan]
    url_scheme: http
    netloc: test.ddg.lws.links.com.au
    path: /api/action/package_create

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

