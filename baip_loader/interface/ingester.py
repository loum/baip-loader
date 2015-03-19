import os
import json
import urllib
import urllib2

from logga.log import log
from filer.files import get_directory_files_list

__all__ = ['Ingester']


class Ingester(object):
    """
    .. attribute:: source_dir

        Absolute path to the directory where mapped JSON files are stored

    """
    _source_dir = None
    _api_key = None
    _csiro_uri = None

    def __init__(self, source_dir=None):
        if source_dir is not None:
            self._source_dir = source_dir

    @property
    def source_dir(self):
        return self._source_dir

    @source_dir.setter
    def source_dir(self, value):
        self._source_dir = value

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def csiro_uri(self):
        return self._csiro_uri

    @csiro_uri.setter
    def csiro_uri(self, value):
        self._csiro_uri = value

    def source_files(self, file_filter=None):
        """Checks :attr:`source_dir` for valid CKAN JSON files.

        **Args:**
            *file_filter*: filter file names against this RE-based
            expression

        **Returns:**
            list of absolute path names to the files found

        """
        files_to_process = []

        if (self.source_dir is None or
           not os.path.isdir(self.source_dir)):
            log.error('Source directory "%s" undefined or missing' %
                      self.source_dir)
        else:
            log.debug('Sourcing files at: %s' % self.source_dir)

        log.debug('filter: %s' % file_filter)
        files_to_process.extend(get_directory_files_list(self.source_dir,
                                                         file_filter))
        log.debug('CKAN JSON files sourced: %s' % files_to_process)

        return files_to_process

    def ingest(self, ckan_json, dry=False):
        """Ingest dataset into CKAN.

        **Args:**
            *ckan_json*: the CKAN JSON ingest structure

            *dry*: only report, do not execute

        **Returns:**

            boolean ``True`` on success, ``False`` otherwise

        """
        log.info('Attempting CKAN ingest ...')

        data_string = urllib.quote(ckan_json)

        log.debug('Preparing request to "%s"' % self.csiro_uri)
        request = urllib2.Request(self.csiro_uri)
        request.add_header('Authorization', self.api_key)

        status = True
        if not dry:
            try:
                response = urllib2.urlopen(request, data_string)
                assert(response.code == 200)

                response_dict = json.loads(response.read())
                assert(response_dict['success'] is True)
            except urllib2.HTTPError as err:
                log.error('Error code|msg: {0}|{1}'.format(err.msg,
                                                           err.headers))
                status = False

        return status
