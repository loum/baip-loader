.. BAIP Loader Interface: Mapper

.. toctree::
    :maxdepth: 2

.. _mapper:

Map
===

The BAIP Loader ``map`` context is responsible for converting the
source CSIRO Metadata XML into JSON that is suitable for
`<data.gov.au>`_ ingest.

.. note::

    See :ref:`ingester` on how to load datasets into CKAN (data.gov.au).

Map Workflow
------------

.. note::

    See :ref:`scraper` on how to source the CSIRO metadata.

CSIRO XML to JSON mapping is achieved via the ``baip-loader`` command
inconjunction with the ``map`` sub-command.  Mapping occurs on
an XML data source (either via network endpoint or local file).

Source CSIRO XML
^^^^^^^^^^^^^^^^

CSIRO XML can be sourced as an incremental step in isolation from the
mapping to CKAN and ingest (this is effectively :ref:`scraper`).  This is
in case you want to evaluate the XML before CKAN ingest.  In this event,
the CSIRO XML will reside on the local filesystem where you can invoke
the mapper against the XML file directly.  This can be achieved with the
``--input-file`` switch.  For example, if your CSIRO XML file is named
``metadata.xml``::

    baip-loader map --input-file metdata.xml

Alternatively, if you are super-confident in the CSIRO XML you can omit
the ``--input-file`` switch and ``baip-loader map`` will source the
CSIRO endpoint directly.  The endpoint parameters will be sourced as per
the :ref:`scraper_configuration`.  This is effectively a ``source`` and
``map`` in one step.

.. warning::

    Be aware that if you source the complete CSIRO XML catalogue at once
    you will have to wait a number of minutes for the transfer process
    to complete

XML Data Extraction
^^^^^^^^^^^^^^^^^^^

As of March 2015, `<data.gov.au>`_ is running CKAN v2.2.  The relevant
API documentation can be referenced `here <http://docs.ckan.org/en/ckan-2.2/api.html#module-ckan.logic.action.create>`_.  The ``create`` module's
``package_create()``  function  is particularly useful as it defines the
basic parameters that are required by CKAN to perform a dataset ingest.
`<data.gov.au>`_ provides a few extensions and customisations to the
default CKAN interface.  The source code for the `<data.gov.au>`_
CKAN customisation can be referenced at `GitHub <https://github.com/datagovau/ckanext-datagovau>`_.  There is also a `CKAN extension 
<https://github.com/datagovau/ckanext-agls>`_ to include AGLS/Dublin Core
minimum metadata (ISO19115 generation).  Within this repository, refer to
`ISO19115 build template <https://github.com/datagovau/ckanext-agls/blob/master/ckanext/agls/templates/package/read.gmd>`_ for the values that we need
to augment the CKAN dataset ingest JSON structure.

.. note::

    A `<data.gov.au>`_ dataset ingest is comprised of two components:

    * CKAN specific metadata -- values that are required by the CKAN
      interface for searching, facetting etc.
    * ISO19115 specific metadata -- values that are required by the
      CKAN ISO19115 build

    The mapper tries to cater for both.

.. _ckan_json:

CKAN Dataset Ingest JSON Format
*******************************

A typical CKAN `<data.gov.au>`_ ingest API JSON structure looks like the
following::

    {
        "owner_org": "c5766f7d-963a-4f30-915e-f1a6f1143301",
        "tags": [
            {
                "name": "inlandWaters"
            },
            {
                "name": "Victoria"
            }
        ],
        "date_updated": "2015-02-10",
        "temporal_coverage_to": null,
        "temporal_coverage_from": null,
        "geospatial_topic": [
            "inlandWaters"
        ],
        "revision_id": "Version 2.1",
        "organization": {
            "title":
                "VIC - Department of Environment and Primary Industries"
        },
        "id": "DD006FCE-BEF5-4377-82AE-2C5A14B50E34",
        "metadata_created": "2014-10-24",
        "publisher":
             "VIC - Department of Environment and Primary Industries",
        "name": "Victorian Aquifer Framework - Salinity",
        "language": "eng",
        "field_of_research": [
            "Victoria"
        ],
        "notes": "[This data and its metadata ...",
        "metadata_modified": "2015-02-10",
        "extras": {
            "telephone": "86362385"
        },
        "spatial": [
            "1",
            "-",
            "-",
            "1"
        ],
        "data_state": "completed",
        "title": "Victorian Aquifer Framework - Salinity",
        "contact_point": "data.vsdl@depi.vic.gov.au",
        "date_released": "2014-10-24",
        "update_freq": "asNeeded"
    }

The JSON is constructed as a series of key/value pairs, where each value
could itself be a key for an extended, nested value.  For configuration
settings, we are only concerned with the top level key.  For example,
``notes``.  The data that will form the ``notes`` key's value needs to be
extracted from the CSIRO XML metadata via rules defined in the
``baip-loader`` configuration.

.. ckan_extraction_rules:

Mapper Data Extraction Rules
****************************

``baip-loader`` configuration parameters can be found in the
``/etc/baip/conf/loader.conf`` file.  Mapper extraction settings are
defined under the ``[ckan_mapper]`` section.  A typical entry follows
the format::

    [ckan_mapper]
    <JSON_key>: <JSON_value_01>,<JSON_value_02>,...

Where:

* ``<JSON_key>`` translates to the CKAN ingest JSON key

* ``<JSON_value_01>`` are the XML element levels to the value

For example::

    notes: gmd:identificationInfo|gmd:MD_DataIdentification|gmd:abstract|gco:CharacterString

Here, the individual element levels are separated by ``|`` starting from
the root element ``gmd:identificationInfo``.

The mapper attempts to construct the JSON nesting based on the source XML
structure.  For example, if the source XML target support a multi-value
arrangement then this will be translated to a list in the JSON.

.. note::

    Some value constructions are hard-wired in the code base.

.. ckan_default_rules:

Mapper Data Defaults
********************

The CKAN ingest JSON consists of default key/value pairs that feature in
all ingest datasets.  For example, the ``owner_org`` key represents the
Bureau of Meteorology ID for the CKAN search facet and is mandatory in the
JSON structure.

All CKAN ingest JSON defaults are defined under the ``[ckan_defaults]``
configuration section.  For example::

    [ckan_defaults]
    owner_org: c5766f7d-963a-4f30-915e-f1a6f1143301

Mapper Validation Rule Sets
***************************

Hopefully, this is a temporary arrangement as it is trying to address
a partial limitation on the CKAN ingest interface around case sensitivity.

Some CKAN ingest values are based on a vocabulary of acceptable terms.
For example, ``geospatial_topic`` terms are based on the
`ABS Fields of Research <http://www.abs.gov.au/ausstats/abs@.nsf/0/6BB427AB9696C225CA2574180004463E>`_ topics field.  The ``[validation_sets]``
configuration section allows you to enter the vocabulary list to validate
against a given JSON key.  For example::

    geospatial_topic: Farming,Biota,Boundaries,Climatology Meteorology and Atmosphere,Economy,Elevation,Environment,Geoscientific information,Health,Imagery base maps and Earth cover,Intelligence and Military,Inland waters,Location,Oceans,Planning and Cadastre,Society,Transportation,Utilities and Communication

In the case of the ``geospatial_topic`` field, it will attempt to change
the case of the vocabulary terms to conform to the CKAN interface.

.. note::

    This detail should really be handled on the CKAN side.  However,
    we do it here to save some time.

Output
******

Once the mapping process completes, ``baip-loader map`` will use the
CSIRO GUID value to construct an output file name and dump the resulting
JSON to the ``baip-loader`` :ref:`mapper_inbound_directory_config`.  For
example::

    /var/tmp/baip-loader/DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json

Configuration
-------------

.. note::

    See :ref:`scraper_configuration` on how to configure the CSIRO
    endpoint

.. _mapper_inbound_directory_config:

Inbound Directory
^^^^^^^^^^^^^^^^^

Found under the ``[ingest]`` section, the ``inbound_dir`` option
defines where the mapper will write out the mapped JSON files to::

    [ingest]
    # "inbound_dir" sets the source directory to read ingest files from
    inbound_dir: /var/tmp/baip-loader

``baip-loader map`` Usage
-------------------------------

::

    $ baip-loader map --help
    usage: baip-loader map [-h] [-i INFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --input-file INFILE
                            Source XML from filename
