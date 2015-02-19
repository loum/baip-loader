import os

import baip_loader
from logga.log import log
from filer.files import get_directory_files_list

__all__ = ['Ingester']


class Ingester(object):
    """
    .. attribute:: source_dir

        Absolute path to the directory where mapped JSON files are stored

    """
    _source_dir = None

    def __init__(self, source_dir=None):
        """
        """
        self._source_dir = source_dir

    @property
    def source_dir(self):
        return self._source_dir

    @source_dir.setter
    def source_dir(self, value):
        self._source_dir = value

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
