.. BAIP Loader Interface: Mapper

.. toctree::
    :maxdepth: 2

.. _mapper:

Map
===

The BAIP Loader ``map`` context is responsible for converting the
source CSIRO Metadata XML into JSON.

Map Workflow
------------

.. note::

    See :ref:`scraper` on how to source the CSIRO metadata.

CSIRO XML to JSON mapping is achieved via the ``baip-loader`` command
inconjunction with the ``map`` sub-command.  Mapping occurs on
an XML data source (either via network endpoint or local file)

Configuration
^^^^^^^^^^^^^

.. note::

    See :ref:`scraper_configuration` on how to configure the CSIRO
    endpoint

``baip-loader map`` Usage
-------------------------------

::

    $ baip-loader map --help
    usage: baip-loader map [-h] [-i INFILE] [-o OUTFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --input-file INFILE
                            Source XML from filename
      -o OUTFILE, --outfile OUTFILE
                            Override output filename
