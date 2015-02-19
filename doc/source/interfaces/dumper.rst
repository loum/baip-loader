.. BAIP Loader Interface: Dumper

.. toctree::
    :maxdepth: 2

.. _dumper:

Dumper
======

The BAIP Loader ``dump`` context is responsible for converting the
CSIRO Metadata XML data structure to JSON.  The resulting JSON should
be in a format that can be consumed by the
`data.gov.au <http://data.gov.au/>`_ ingest endpoint.

The CSIRO XML root is the ``BaMetadataRecords`` element.  It can contain
1 or more ``MD_Metadata`` nested items.  Each ``MD_Metadata`` item results
in a separate JSON file.  For uniqueness, the name of the file is based
on the CSIRO GUID which is extracted from the XML in a preliminary step.

Dumper Workflow
----------------

Extraction
^^^^^^^^^^
The sourcing of CSIRO metadata is achieved via the ``baip-loader`` command
inconjunction with the ``dump`` sub-command.  ``dump`` context is
aimed at being a preliminary step to the ``load`` context.

CSIRO metadata can sourced directly from the CSIRO HTTP-based endpoint
(see :ref:`scraper`) or from a file located directly on the local
filesystem.  Sourcing the the complete metadata set from the CSIRO
HTTP-based endpoint can be time consuming so you probably only want to do
this once and then work with the local copy.

Mapping
^^^^^^^
.. todo::

    Provide high level summary of the mapping context

JSON File Generation
^^^^^^^^^^^^^^^^^^^^
Typical organisation of the generated files is as follows::

    $ ls -1 /var/tmp/baip-loader/
    457ED79A-C6DF-4AAF-A480-00926E48CAA8.json
    6151C409-0CAF-4727-9F57-00F6B71A58FB.json
    6968B11F-9912-42CA-8536-00CDE75E75D9.json
    781A8B81-93B8-4CDE-9B56-00291D7543EA.json
    DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json

In the above example, the target path has been configured as
``/var/tmp/baip-loader``.  However, this can be altered via
:ref:`dumper_configuration`.

.. _dumper_configuration:

Configuration
-------------

.. note::

    See :ref:`csiro_metadata_endpoint_configuration` for the settings that
    control the enpoint parameters.

JSON File Target Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^
Mapped JSON files are placed under the ``inbound_dir`` configuration
item::

    inbound_dir: /var/tmp/baip-loader

``baip-loader dump`` Usage
--------------------------

::

    $ baip-loader dump --help
    usage: baip-loader dump [-h] [-i INFILE]

    optional arguments:
        -h, --help            show this help message and exit
        -i INFILE, --input-file INFILE
                              Source XML from filename

