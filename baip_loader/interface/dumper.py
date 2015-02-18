import os

import baip_loader
from logga.log import log

__all__ = ['Dumper']


class Dumper(object):
    """:class:`baip_loader.Dumper`

    """
    _target_dir = None

    def __init__(self, target_dir=None):
        """
        """
        self._target_dir = target_dir

    @property
    def target_dir(self):
        return self._target_dir

    @target_dir.setter
    def target_dir(self, value):
        self._target_dir = value

    def dump(self, uri=None, infile=None):
        loader = baip_loader.Loader()

        loader.csiro_source_uri = uri
        loader.source(filename=infile)
        outfiles = loader.extract_guids(to_json=True)

        files_produced = []
        for filename, contents in outfiles:
            target_file = os.path.join(self.target_dir, filename + '.json')
            files_produced.append(target_file)
            log.info('Writing output to JSON file: %s' % target_file)
            target_fh = open(target_file, 'w')
            target_fh.write(contents)
            target_fh.close()

        return files_produced
