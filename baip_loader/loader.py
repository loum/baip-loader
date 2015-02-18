import urllib2
import tempfile
import xmltodict
import json

from logga.log import log


__all__ = ["Loader"]


class Loader(object):
    """:class:`baip_loader.Loader`

    .. attribute:: *csiro_source_uri*

    .. attribute:: *csiro_source_data*

    """
    _csiro_source_uri = None
    _csiro_source_data = None

    def __init__(self, source_uri=None):
        """
        """
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
                        guid = self.extract_guid(item)
                        if guid is not None:
                            item_as_json = None
                            if to_json:
                                item_as_json = json.dumps(item)

                            yield (guid, item_as_json)

    def extract_guid(self, md_metadata):
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
