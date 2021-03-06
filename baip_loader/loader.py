import urllib2
import tempfile
import xmltodict
import json
import geojson
import shapely.geometry

from logga.log import log

__all__ = ["Loader"]


class Loader(object):
    """
    .. attribute:: csiro_source_uri

        CSIRO XML-based metadata endpoint

    .. attribute:: csiro_source_data

        Memory resident copy of the sourced CSIRO XML-based metadata

    .. attribute:: ckan_mapper

    .. attribute:: ckan_defaults

    """
    _csiro_source_uri = None
    _csiro_source_data = None
    _ckan_mapper = {}
    _validation_sets = {}
    _ckan_defaults = {}

    def __init__(self, source_uri=None):
        if source_uri is not None:
            self._csiro_source_uri = source_uri

    @property
    def csiro_source_uri(self):
        return self._csiro_source_uri

    @csiro_source_uri.setter
    def csiro_source_uri(self, value):
        self._csiro_source_uri = value

    @property
    def csiro_source_data(self):
        return self._csiro_source_data

    @csiro_source_data.setter
    def csiro_source_data(self, value):
        self._csiro_source_data = value

    @property
    def ckan_mapper(self):
        return self._ckan_mapper

    @ckan_mapper.setter
    def ckan_mapper(self, values=None):
        self._ckan_mapper.clear()

        if values is not None and isinstance(values, dict):
            self._ckan_mapper = values

    @property
    def validation_sets(self):
        return self._validation_sets

    @validation_sets.setter
    def validation_sets(self, values=None):
        self._validation_sets.clear()

        if values is not None and isinstance(values, dict):
            self._validation_sets = values

    @property
    def ckan_defaults(self):
        return self._ckan_defaults

    @ckan_defaults.setter
    def ckan_defaults(self, values=None):
        self._ckan_defaults.clear()

        if values is not None and isinstance(values, dict):
            self._ckan_defaults = values

    def source(self, filename=None):
        """Attempt to source CSIRO metadata.

        If *filename* is provided, then file will be opened and contents
        parsed.  Otherwise, an attempt will be made to connect to the
        :attr:`csiro_source_uri` endpoint.

        .. note::

            The entire metadata set is stored in memory and can be
            accessed via the :attr:`csiro_source_data` attribute

        **Args:**
            *filename*: override source endpoint with filename

        """
        log.info('Sourcing data ...')

        source = filename
        if source is None:
            source = self.csiro_source_uri
            log.debug('Connecting to "%s"' % source)
            url_obj = urllib2.urlopen(self.csiro_source_uri)
            self.csiro_source_data = url_obj.read()
        else:
            source_fh = open(source)
            self.csiro_source_data = source_fh.read()
            source_fh.close()

        msg = 'Data sourced from {source}'
        log.debug(msg.format(source=source))

    def dump_source(self, filename=None):
        """Write out the contents of the :attr:`csiro_source_data`
        to *filename* if not `None` or a temporary file using
        :mod:`tempfile.NamedTemporaryFile`.

        if :attr:`csiro_source_data` is `None` then no attempt to write
        will be made.

        **Args:**
            *filename*: full path of the target file to write to

        **Returns:**
            On write success, the name of the output filename.  ``None``
            otherwise

        """
        file_obj = None
        target_file = None

        if self.csiro_source_data is not None:
            if filename is None:
                file_obj = tempfile.NamedTemporaryFile(delete=False)
            else:
                file_obj = open(filename, 'w')

            target_file = file_obj.name

            log.info('Writing CSIRO content to {0}'.format(target_file))
            file_obj.write(self.csiro_source_data)
            file_obj.close()
        else:
            log.info('Source data not defined -- skipping write')

        return target_file

    def translate(self):
        """Extract and translate the source :attr:`csiro_source_data`
        ISO19115 XML elements to a CKAN ingestable data structure format.

        if :attr:`csiro_source_data` is `None` then no attempt to extract
        will be made.

        **Returns:**
            dictionary structure of the form::

                {<guid_01>: <ckan_ingest_data_01>,
                 <guid_02>: <ckan_ingest_data_02>, ...}

        """
        ckan_data = {}

        if self.csiro_source_data is None:
            log.info('Source data not defined -- skipping write')
        else:
            xml_as_dict = xmltodict.parse(self.csiro_source_data)

            # Only interested in the "BaMetadataRecords" element.
            ba_metadata_records = xml_as_dict.get('BaMetadataRecords')
            if ba_metadata_records is None:
                log.error('Unable source BaMetadataRecords root element')
            else:
                md_metadata = ba_metadata_records.get('gmd:MD_Metadata')
                if md_metadata is not None:
                    log.debug('md_metadata is not None')
                    if isinstance(md_metadata, dict):
                        # Fudge value into list so that we can apply a
                        # single processing logic stream.
                        md_metadata = [md_metadata]

                    for item in md_metadata:
                        guid = Loader.extract_guid(item)
                        if guid is None:
                            log.warn('Unable to extract GUID')
                            continue

                        log.debug('Processing GUID: "%s" ...' % guid)
                        ckan_mapped = self.iso19115_to_ckan_map(item)
                        ckan_sanitised = self.sanitise(ckan_mapped)
                        ckan_reformatted = self.reformat(ckan_sanitised)
                        ckan_validated = self.validate(ckan_reformatted)
                        ckan = self.add_ckan_defaults(ckan_validated)
                        ckan_data[guid] = ckan
                        log.debug('GUID "%s" complete' % guid)

        return ckan_data

    def extract_guids(self, xml_data=None, to_json=False):
        """Cycle through the :attr:`csiro_source_data` XML data structure

        CSIRO XML root is the ``BaMetadataRecords`` element.  It can
        contain 1 or more ``MD_Metadata`` nested items.  Here, we support
        both types of nested structures.

        **Returns**:
            a list of all extracted CSIRO GUIDs

        """
        if self.csiro_source_data is not None:
            xml_data = self.csiro_source_data

        if xml_data is None:
            xml_data = {}

        xml_dict = xmltodict.parse(xml_data)

        # Only interested in the "BaMetadataRecords" element.
        ba_metadata_records = xml_dict.get('BaMetadataRecords')
        if ba_metadata_records is None:
            log.error('Unable source BaMetadataRecords root element')
        else:
            md_metadata = ba_metadata_records.get('gmd:MD_Metadata')
            if md_metadata is not None:
                if isinstance(md_metadata, dict):
                    # Fudge value into list so that we can apply a single
                    # processing logic stream.
                    md_metadata = [md_metadata]

                if isinstance(md_metadata, list):
                    for item in md_metadata:
                        guid = Loader.extract_guid(item)
                        if guid is not None:
                            item_as_json = None
                            if to_json:
                                item_as_json = json.dumps(item)

                            yield (guid, item_as_json)

    @staticmethod
    def extract_guid(md_metadata):
        """Contains the logic that manages the actual nested
        ``gco:CharacterString`` (or CSIRO GUID) extraction.

        **Args:**
            *md_metadata*:
                the CSIRO nested ``gmd:MD_Metadata`` item as a Python
                dictionary strucutre.  For example::

                    {
                        'gmd:MD_Metadata': {
                            'gmd:fileIdentifier': {
                                'gco:CharacterString':
                                    'DD006FCE-BEF5-4377-82AE-2C5A14B50E34'
                             }
                        }
                    }

        **Returns:**
            the CSIRO Metadata GUID upon success.  ``None`` otherwise.

        """
        guid = None

        file_id = md_metadata.get('gmd:fileIdentifier')
        if file_id is None:
            log.error('Unable to source "gmd:fileIdentifier"')
        else:
            guid = file_id.get('gco:CharacterString')

        return guid

    @staticmethod
    def xml2json(xml):
        """Convert the *xml* data structure to JSON.

        **Args:**
            *xml*: the XML data structure to convert to JSON

        **Returns:**
            The JSON equivalent of *xml*

        """
        json_data = xmltodict.parse(xml)

        return json.dumps(json_data)

    @staticmethod
    def extract_iso19115_field(levels, csiro_json):
        """Recursively drill into *csiro_json* dictionary based on the
        number of *levels*.

        **Args:**
            *levels*: list of keys used to drill into the nested
            dictionary

            *csiro_json*: branch of the ISO19115 dictionary structure

        **Returns:**
            On the last call, the dictionary key's value

        """
        level = levels.pop(0)
        log.debug('Extracting level: %s' % level)

        nest = None

        if isinstance(csiro_json, dict):
            nest = csiro_json.get(level)
        elif isinstance(csiro_json, list):
            nest = [i.get(level) for i in csiro_json if isinstance(i, dict)]

        if len(levels) > 0 and nest is not None:
            nest = Loader.extract_iso19115_field(levels, nest)

        return nest

    def iso19115_to_ckan_map(self, csiro_json_data):
        """Pull out the required CKAN fields from the source
        *csiro_json_data*.

        **Args:**
            *csiro_json_data*: the source ISO19115 data (in a dictionary
            data structure representation)

        **Returns:**
            the CKAN data in a dictionary of lists structure

        """
        ckan_data = {}

        for key, values in self.ckan_mapper.iteritems():
            log.info('Performing map for CKAN field: "%s"' % key)

            field_values = []
            for value in values:
                log.debug('Nest: %s' % value)
                levels = value.split('|')
                field_value = Loader.extract_iso19115_field(levels,
                                                            csiro_json_data)
                field_values.append(field_value)

            ckan_data[key] = field_values

        return ckan_data

    @staticmethod
    def extract_iso19115_dates(iso19115_dates):
        """The ISO19115 XML dates come through in a convuluted format, I
        think targeted towards some kind of XPath extraction.  Because
        we ditch XML in favor of JSON at the earliest possible
        opportunity (i.e. step 1) we are left with an awkward
        dictionary structure.  (I really don't understand the reason for
        embedding such complexity in this structure -- madness!)

        This method tries to untangle the ISO19115 date structure and
        return a sane dictionary representation of the creation,
        publication and revision dates in the format::

            {'publication': '<YYYY-MM-DD>',
             'revision': '<YYYY-MM-DD>',
             'creation': '<YYYY-MM-DD>'}

        **Args:**
            *iso19115_dates*: list of nested ISO19115 ``gmd:CI_Date``
            elements.  For example::

                [
                    {
                        'gmd:CI_Date': {
                            'gmd:date': {
                                'gco:Date': '2015-02-10'
                            },
                            'gmd:dateType': {
                                'gmd:CI_DateTypeCode': {
                                    '#text': 'creation',
                                    '@codeList': 'http://asdd.ga.gov.au...',
                                    '@codeListValue': 'creation'
                                }
                            }
                        }
                    }
                ]

        **Returns:**
            creation, publication and revision dates in the format::

                {'publication': '<YYYY-MM-DD>',
                 'revision': '<YYYY-MM-DD>',
                 'creation': '<YYYY-MM-DD>'}

        """
        type_code_levels = ['gmd:CI_Date',
                            'gmd:dateType',
                            'gmd:CI_DateTypeCode',
                            '#text']
        date_levels = ['gmd:CI_Date',
                       'gmd:date',
                       'gco:Date']

        dates = {}

        log.debug('iso19115_dates: %s' % iso19115_dates)
        for ci_date in iso19115_dates[0]:
            levels = list(type_code_levels)
            date_type = Loader.extract_iso19115_field(levels, ci_date)

            if date_type in ['creation', 'revision', 'publication']:
                levels = list(date_levels)
                date = Loader.extract_iso19115_field(levels, ci_date)
                dates[date_type] = date

        log.debug('Dates extracted from iso19115_dates: "%s"' % dates)

        return dates

    def sanitise(self, ckan_data):
        """The ISO19115 to CKAN extraction phase is a simple lookup of XML
        element names and requires further consolidation via this
        sanitisation phase so that it conforms to the CKAN ingest API
        format.

        **Args:**
            *ckan_data*:

        **Returns:**

        """
        sanitise_data = dict(ckan_data)

        # Dates.
        if ckan_data.get('dates') is not None:
            dates = self.extract_iso19115_dates(sanitise_data.pop('dates',
                                                                  None))
            sanitise_data['date_released'] = dates.get('publication')
            sanitise_data['metadata_created'] = dates.get('publication')
            sanitise_data['date_updated'] = dates.get('revision')

        # Spatial.
        spatial_data = Loader.extract_iso19115_spatial(sanitise_data)
        sanitise_data.clear()
        sanitise_data = spatial_data

        # temporal_coverage_*
        coverage_from = ckan_data.get('temporal_coverage_from')
        if coverage_from is not None:
            sanitise_data['temporal_coverage_from'] = coverage_from[0]

        coverage_to = ckan_data.get('temporal_coverage_to')
        if coverage_to is not None:
            sanitise_data['temporal_coverage_to'] = coverage_to[0]

        # revision_id
        revision_id = ckan_data.get('revision_id')
        if revision_id is not None:
            sanitise_data['revision_id'] = revision_id[0]

        # Topic Category
        topic_category = ckan_data.get('geospatial_topic')
        if (topic_category is not None and
           not isinstance(topic_category[0], list)):
            sanitise_data['geospatial_topic'] = [topic_category]

        return sanitise_data

    @staticmethod
    def extract_iso19115_spatial(ckan_data):
        """There are multiple ISO19115 spatial formats which include
        polygons and bounding boxes.  However, the CKAN interface
        only provides an allocation for a single spatial type.

        The CKAN spatial type supports points, polygons, bounding boxes
        or a free-text Gazetteer type URL.  This method cycles through the
        ISO19115 spatial types and identifies the target source value to
        use.  The output format will be based on the spatial type used.

        At this time, the method supports polygons and bounding boxes
        with polygons having precedence over bounding boxes.

        .. note::

            You may note in the CKAN interface that spatial
            data is referenced as ``spatial`` and ``spatial_coverage``.

            * ``spatial`` is the data used to build the `<data.gov.au>`_
              ISO19115 spatial information.  This data must be presented
              as GeoJSON (see `GeoJSON validation rules
              <http://geojsonlint.com/>`_)

            * ``spatial_coverage`` is used by the `<data.gov.au>`_
              interface's spatial sub-system (if the plugin is enabled).
              This is used by `<data.gov.au>`_ for spatial queries and
              visualisations.  This data must be presented in WKT format

        **Args:**
            *ckan_data*:

        **Returns:**
            the modified *ckan_data* data structure with spatial content
            modified as per the business rules

        """
        spatial_reduced_data = dict(ckan_data)
        spatial = spatial_reduced_data['spatial'] = []

        bbox = [spatial_reduced_data.get('bbox_east'),
                spatial_reduced_data.get('bbox_north'),
                spatial_reduced_data.get('bbox_south'),
                spatial_reduced_data.get('bbox_west')]
        if None not in bbox:
            for index in range(0, 4):
                if (not Loader.empty(bbox[index])):
                    spatial.append(bbox[index][0][0])
                else:
                    spatial_reduced_data.pop('spatial', None)
                    break

            # Set the CKAN ISO19115 spatial field.
            bbox = None
            if spatial_reduced_data.get('spatial') is not None:
                bbox = spatial

        log.debug('Checking for polygon data ...')
        if (spatial_reduced_data.get('polygon') is not None and
           not Loader.empty(spatial_reduced_data.get('polygon'))):
            polygon = spatial_reduced_data['polygon']
            log.debug('Polygon data found: %s' % polygon)

            geojson_polygon = wkt_polygon = None
            if polygon[0] is not None:
                geojson_polygon = Loader.reformat_polygon(polygon)
                wkt_polygon = Loader.geojson_to_wkt(geojson_polygon)

                spatial_reduced_data['spatial'] = json.dumps(geojson_polygon)
                spatial_reduced_data['spatial_coverage'] = wkt_polygon
        else:
            log.debug('Checking for bounding box data ...')
            if not Loader.empty(spatial):
                geojson_bbox = Loader.reformat_bbox(bbox)
                log.debug('Bounding box data found: %s' %
                          json.dumps(geojson_bbox))
                spatial_reduced_data['spatial'] = json.dumps(geojson_bbox)

        # Remove temporary spatial values.
        for key in ['polygon',
                    'bbox_east',
                    'bbox_north',
                    'bbox_west',
                    'bbox_south']:
            spatial_reduced_data.pop(key, None)

        # Remove if no data found.
        if Loader.empty(spatial):
            spatial_reduced_data.pop('spatial', None)

        return spatial_reduced_data

    @staticmethod
    def empty(seq):
        for item in seq:
            if not isinstance(item, list) or not Loader.empty(item):
                return False

        return True

    @staticmethod
    def reformat(sanitised_ckan_data):
        """Checks *sanitised_ckan_data* for nested lists of values and
        makes a best estimate as to whether the values should present
        to CKAN as a list of values or as a string.

        Also invokes the :meth:`reformat_keys` to convert the
        multi-level keys into a nested dictionary structure.

        .. note::

            CKAN data formatting should occur after the craziness of the
            CSIRO XML has passed through :meth:`Loader.sanitise`.

        **Args:**
            *sanitised_ckan_data*: the sanitised CKAN data structure

        **Returns:**
            the re-formatted CKAN data ready for ingest

        """
        formatted_ckan_data = dict(sanitised_ckan_data)

        for field, value in sanitised_ckan_data.iteritems():
            if value is None:
                continue

            nested = False
            if not any(isinstance(el, list) for el in value):
                # This is a single item.
                if isinstance(value, list) and len(value):
                    if value[0] is None:
                        formatted_ckan_data.pop(field, None)
                    else:
                        formatted_ckan_data[field] = value[0]
            else:
                values = Loader.flatten(value)
                nested = True
                formatted_ckan_data[field] = list(values)

            log.debug('field "%s" nested? %s' % (field, nested))

        formatted_ckan_keys = dict(formatted_ckan_data)
        formatted_ckan_data = Loader.reformat_keys(formatted_ckan_keys)

        # Probably better to drive this via configuration, but
        # hard-wiring data reformatting here ...
        #
        # Tags.
        if formatted_ckan_keys.get('tags') is not None:
            tags = formatted_ckan_keys.get('tags')

            new_tags = []
            for tag in tags:
                new_tags.append({'name': tag})

            del formatted_ckan_keys['tags'][:]
            formatted_ckan_keys['tags'].extend(new_tags)

        return formatted_ckan_data

    @staticmethod
    def reformat_keys(formatted_ckan_data):
        """Cycle through the keys provided by *formatted_ckan_data*
        and change a multi-part key values into a nested
        dictionary structure.  A multi-part key value is denoted
        by a separating ``|``.  For example::

            # Old
            DATA = {
                'organization|title': 'Geoscience Australia'
            }

        ::

            # New
            DATA = {
                'organization': {
                    'title': 'Geoscience Australia'
                }
            }

        **Args:**
            *formatted_ckan_data*:

        **Returns:**
            the re-formated data structure with nested keys (if required)

        """
        formatted_keys = dict(formatted_ckan_data)

        for keys, value in formatted_keys.iteritems():
            nests = keys.split('|')
            if len(nests) > 1:
                tmp = reduce(lambda x, y: {y: x}, reversed(nests + [value]))
                log.debug('Reformated key: "%s" to "%s"' % (keys, tmp))
                formatted_keys.pop(keys, None)
                formatted_keys.update(tmp)

        return formatted_keys

    @staticmethod
    def flatten(container):
        for i in container:
            if i is None:
                continue

            if isinstance(i, list) or isinstance(i, tuple):
                for j in Loader.flatten(i):
                    yield j
            else:
                yield i

    def validate(self, ckan_data):
        """Some extra formatting of *ckan_data* must be occur
        to fully comply with the CKAN ingest API.  For example, the
        research fields must align with the list provided by the
        Australian Bureau of Statistics.

        **Args:**
            *ckan_data*:

        **Returns:**
            a fully CKAN ingest compliant data structure.

        """
        validated_ckan_data = dict(ckan_data)

        # CKAN name field must be all lower case.
        name_field = validated_ckan_data.get('name')
        if name_field is not None:
            log.debug('CKAN name field found: "%s"' % name_field)
            validated_ckan_data['name'] = name_field.lower()
            log.debug('CKAN name field converted to: "%s"' %
                      validated_ckan_data['name'])

        for key in self.ckan_mapper.keys():
            log.debug('Validating field: "%s"' % key)

            if self.validation_sets.get(key) is None:
                log.debug('Validation set does not exist for "%s"' % key)
                continue

            validation_set = self.validation_sets.get(key)
            data = ckan_data.get(key)
            log.debug('Validation check <key>|<data>: "%s"|"%s"' %
                      (key, data))

            if isinstance(data, basestring):
                for validation_set_item in validation_set:
                    if data.lower() == validation_set_item.lower():
                        log.debug('Validation match: %s' %
                                  validation_set_item)
                        validated_ckan_data[key] = validation_set_item
            elif isinstance(data, list):
                data_values = list(data)
                for item in data:
                    for validation_set_item in validation_set:
                        if item.lower() == validation_set_item.lower():
                            data_values.remove(item)
                            data_values.append(validation_set_item)
                            log.debug('Validation match: %s' %
                                      validation_set_item)
                validated_ckan_data[key] = data_values

        return validated_ckan_data

    def add_ckan_defaults(self, ckan_reformatted_data):
        """Cycles through the :attr:`ckan_defaults` and augments
        the *ckan_reformatted_data* with the :attr:`ckan_defaults`
        key value pairs.

        .. note::
            assumes that *ckan_reformatted_data* has already
            passed through the :meth:`reformat` method

        **Args:**
            *ckan_reformatted_data*: the reformatted CKAN data structure

        **Returns:**
            new augmented dictionary structure between
            *ckan_reformatted_data* and the :attr:`ckan_defaults`

        """
        ckan_data = dict(ckan_reformatted_data)

        for key, value in self.ckan_defaults.iteritems():
            log.debug('Added ckan_defaults:%s ' % key)
            ckan_data[key] = value

        return ckan_data

    @staticmethod
    def geojson_to_wkt(geo):
        """Simple helper method to convert geospatial *geo* to WKT.

        **Args:**
            *geo*: source GeoJSON to convert

        **Returns:**
            WKT representation of GeoJSON source

        """
        log.debug('GeoJSON %s to WKT conversion ...' % json.dumps(geo))

        geo_json = geojson.loads(json.dumps(geo))

        geo_shape = shapely.geometry.shape(geo_json)
        log.debug('WKT result: %s' % geo_shape.wkt)

        return geo_shape.wkt

    @staticmethod
    def reformat_polygon(polygon):
        """Reformat the ISO19115 polygon to GeoJSON.

        **Args:**
            *polygon*: nested list structure of the form::

                [[['110.0012 -10.00117', '115.008 -10.00117', ...]]]

        **Returns:**
            GeoJSON representation of the polygon.  For example::

                {
                    'type': 'Polygon',
                    'coordinates': [
                        [
                            [110.0012, -10.00117],
                            [115.008, -10.00117],
                            [155.008, -45.00362],
                            [110.0012, -45.00362],
                            [110.0012, -10.00117],
                        ],
                    ],
                }

        """
        log.debug('Converting ISO19115 polygon %s to GeoJSON ...' % polygon)
        geo_json = {
            'type': 'Polygon',
            'coordinates': [
                    [[float(c) for c in p.split()] for p in polygon[0][0]],
            ]
        }

        log.debug('Resultant GeoJSON polygon: %s' % geo_json)

        return geo_json

    @staticmethod
    def reformat_bbox(bbox):
        """Reformat the ISO19115 bounding box to GeoJSON.

        **Args:**
            *bbox*: list structure of the form::

                ['155.008', '-10.00117', '-45.00362', '110.0012']

        **Returns:**
            GeoJSON representation of the bounding box.  For example::

                {
                    'type': 'Feature',
                    'bbox': [
                        155.008,
                        -10.00117,
                        -45.00362,
                        110.0012
                    ],
                }

        """
        log.debug('Converting ISO19115 bbox %s to GeoJSON ...' % bbox)
        geo_json = {
            'type': 'Feature',
            'bbox': [float(p) for p in bbox],
        }

        log.debug('Resultant GeoJSON bbox: %s' % geo_json)

        return geo_json
