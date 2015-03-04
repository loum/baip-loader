import urllib2
import tempfile
import xmltodict
import json

from logga.log import log


__all__ = ["Loader"]


class Loader(object):
    """
    .. attribute:: csiro_source_uri

        CSIRO XML-based metadata endpoint

    .. attribute:: csiro_source_data

        Memory resident copy of the sourced CSIRO XML-based metadata

    .. attribute:: ckan_mapper

    """
    _csiro_source_uri = None
    _csiro_source_data = None
    _ckan_mapper = {}

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

    def dump_translated(self, filename=None):
        """Write out the contents of the :attr:`csiro_source_data`
        to *filename* if not `None` or a temporary file using
        :mod:`tempfile.NamedTemporaryFile` as JSON.

        XML to JSON translation is implied.

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
            file_obj.write(self.xml2json(self.csiro_source_data))
            file_obj.close()
        else:
            log.info('Source data not defined -- skipping write')

        return target_file

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
    def extract_iso19115_field(levels, xml_data):
        """Recursively drill into *xml_data* dictionary based on the
        number of *levels*.

        **Args:**
            *levels*: list of keys used to drill into the nested
            dictionary

            *xml_data*: branch of the ISO19115 dictionary structure

        **Returns:**
            On the last call, the dictionary key's value

        """
        level = levels.pop(0)
        log.debug('Extracting level: %s' % level)

        nest = None

        if isinstance(xml_data, dict):
            nest = xml_data.get(level)
        elif isinstance(xml_data, list):
            nest = [i.get(level) for i in xml_data if isinstance(i, dict)]

        if len(levels) > 0 and nest is not None:
            nest = Loader.extract_iso19115_field(levels, nest)

        return nest

    def iso19115_to_ckan_map(self, xml_data):
        """Pull out the required CKAN fields from the source *xml_data*.

        **Args:**
            *xml_data*: the source ISO19115 data (in a dictionary
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
                                                            xml_data)
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
            sanitise_data['date_updated'] = dates.get('revision')

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

        **Args:**
            *ckan_data*:

        **Returns:**
            the modified *ckan_data* data structure with spatial content
            modified as per the business rules

        """
        spatial_reduced_data = dict(ckan_data)

        log.debug('Checking for polygon data ...')
        if (spatial_reduced_data.get('polygon') is not None and
           not Loader.empty(spatial_reduced_data.get('polygon'))):
            polygon = spatial_reduced_data['polygon']
            spatial_reduced_data['spatial_coverage'] = polygon
            log.debug('Polygon data found: %s' % polygon)
        else:
            log.debug('Checking for bounding box data ...')
            bbox = [spatial_reduced_data.get('bbox_east'),
                    spatial_reduced_data.get('bbox_north'),
                    spatial_reduced_data.get('bbox_south'),
                    spatial_reduced_data.get('bbox_west')]
            if None not in bbox:
                spatial = spatial_reduced_data['spatial_coverage'] = []
                for index in range(0, 4):
                    if (not Loader.empty(bbox[index])):
                        spatial.append(bbox[index][0][0])
                    else:
                        del spatial[:]
                        spatial_reduced_data.pop('spatial_coverage', None)
                        break

                if not Loader.empty(spatial):
                    log.debug('Bounding box data found: %s' % bbox)

        # Remove temporary spatial values.
        for key in ['polygon',
                    'bbox_east',
                    'bbox_north',
                    'bbox_west',
                    'bbox_south']:
            spatial_reduced_data.pop(key, None)

        return spatial_reduced_data

    @staticmethod
    def empty(seq):
        for item in seq:
            if not isinstance(item, list) or not Loader.empty(item):
                return False

        return True
