.. BAIP Loader Interface: Scraper

.. toctree::
    :maxdepth: 2

.. _scraper:

Scraper
=======

The BAIP Loader scrape context is responsible for connecting to the
source endpoint at CSIRO and "scraping" (or extracting the metadata)
from the target resource.

The CSIRO endpoint offers a ISO19115 records that can be accessed
as a complete set or as inidividual records.  The records themselves are
identified with a GUID.  For example,
``DD006FCE-BEF5-4377-82AE-2C5A14B50E34``.

Since the bulk download can be time consuming (~5 minutes) you can provide
a file name to the ``--output-file`` parameter and the BAIP Loader scrape
context will simply write the CSIRO contents to that file.  By default this
file will be ``csiro_metadata.xml`` in the current directory.  This can act
as a local cache for further processing by specifying the
``csiro_metadata.xml`` BAIP Loader :ref:`mapper` context as the
``--input-file`` parameter.  This will save you some time.

Scraper Workflow
----------------

The sourcing of CSIRO metadata is achieved via the ``baip-loader`` command
inconjunction with the ``scrape`` sub-command.

.. _scraper_configuration:

Configuration
-------------

.. _csiro_metadata_endpoint_configuration:

CSIRO Metadata Endpoint
^^^^^^^^^^^^^^^^^^^^^^^
``baip-loader scrape`` context takes its runtime parameters from the
``/etc/baip/conf/loader.conf`` file.  The CSIRO target endpoint
can be configured under the ``[csiro]`` section.  The supported settings
form the general structure of the URL in the format::

    scheme://netloc/path?query

For example, the following configuration is assocated with the URL
``http://data.bioregionalassessments.gov.au/function/metadataexport``::

    [csiro]
    url_scheme: http
    netloc: data.bioregionalassessments.gov.au
    path: /function/metadataexport
    query:

.. note::

    The CSIRO endpoint does not use the query parameters in the
    construction of the URI.  However, you are able to specify
    individual records by appending the GUID to the path.  For example::

        [csiro]
        url_scheme: http
        netloc: data.bioregionalassessments.gov.au
        path: /function/metadataexport/DD006FCE-BEF5-4377-82AE-2C5A14B50E34
        query:

``baip-loader scrape`` Usage
----------------------------

::

    $ baip-loader scrape --help
    usage: baip-loader scrape [-h] [-o OUTFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --input-file INFILE
                            Source XML from filename
      -o OUTFILE, --outfile OUTFILE
                            Override output filename

