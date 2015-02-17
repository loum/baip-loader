.. BAIP Loader Interface: Scraper

.. toctree::
    :maxdepth: 2

.. _scraper:

Scraper
=======

The BAIP Loader scrape context is responsible for connecting to the
source endpoint at CSIRO and "scraping" the target metadata.

Scraper Workflow
----------------

The sourcing of CSIRO metadata is achieved via the ``baip-loader`` command
inconjunction with the ``scrape`` sub-command.

.. _scraper_configuration:

Configuration
^^^^^^^^^^^^^
``baip-loader`` scrape context takes its runtime parameters from the
``/etc/baip/conf/loader.conf`` file.  The CSIRO target endpoint
can be configured under the ``[csiro]`` section.  The supported settings
form the general structure of the URL in the format::

    scheme://netloc/path?query

For example, the following configuration is assocated with the URL
``http://data.bioregionalassessments.gov.au/function/metadataexport``::

    [csiro]
    url_scheme: http
    netloc: data.bioregionalassessments.gov.au
    path: function/metadataexport
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

