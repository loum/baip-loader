.. BAIP Loader Interface: Translator

.. toctree::
    :maxdepth: 2

.. _translator:

Translator
==========

The BAIP Loader ``translator`` context is responsible for converting the
source CSIRO Metadata XML into JSON.

Translator Workflow
-------------------

.. note::

    See :ref:`scraper` on how to source the CSIRO metadata.

CSIRO XML to JSON translation is achieved via the ``baip-loader`` command
inconjunction with the ``translator`` sub-command.  Translation occurs on
an XML data source (either via network endpoint or local file)

Configuration
^^^^^^^^^^^^^

.. note::

    See :ref:`scraper_configuration` on how to configure the CSIRO
    endpoint

``baip-loader translate`` Usage
-------------------------------

::

    $ baip-loader translate --help
    usage: baip-loader translate [-h] [-i INFILE] [-o OUTFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --input-file INFILE
                            Source XML from filename
      -o OUTFILE, --outfile OUTFILE
                            Override output filename
