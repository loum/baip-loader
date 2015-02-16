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

    def source(self):
        """Attempt to source CSIRO metadata.

        .. note::

            The entire metadata set is stored in memory and can be
            accessed via the :attr:`csiro_source_data` attribute

        """
        msg = 'Sourcing data from {uri} ...'
        log.debug(msg.format(uri=self.csiro_source_uri))

        url_obj = urllib2.urlopen(self.csiro_source_uri)
        self.csiro_source_data = url_obj.read()

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
