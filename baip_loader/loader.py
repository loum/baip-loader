# pylint: disable=R0903,C0111,R0902
"""The :class:`baip_loader.Loader` provides file ingest support.

"""
__all__ = ["Loader"]

import urllib2

from logga.log import log


class Loader(object):
    """:class:`baip_loader.Loader`

    _csiro_source_uri = None

    """
    def __init__(self, source_uri=None):
        """
        """
        if source_uri is not None:
            self._csiro_source_uri = source_uri

    @property
    def csiro_source_uri(self):
        return self._csiro_source_uri

    @csiro_source_uri.setter
    def set_csiro_source_uri(self, value):
        self._csiro_source_uri = value

    def source(self):
        """Attempt to source CSIRO metadata.

        """
        msg = 'Sourcing data from {uri} ...'
        log.debug(msg.format(uri=self.csiro_source_uri))

        url_obj = urllib2.urlopen(self.csiro_source_uri)
        content = url_obj.read()

        import tempfile
        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_obj.write(content)
        file_obj.close()
