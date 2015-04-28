import os
import json

import baip_loader
from logga.log import log

__all__ = ['Mapper']


class Mapper(object):
    """:class:`baip_loader.Mapper`

    """
    _target_dir = None
    _loader = baip_loader.Loader()

    def __init__(self, target_dir=None):
        if target_dir is not None:
            self._target_dir = target_dir

    @property
    def target_dir(self):
        return self._target_dir

    @target_dir.setter
    def target_dir(self, value):
        self._target_dir = value

    @property
    def loader(self):
        return self._loader

    def xml_to_ckan_map(self, uri=None, infile=None):
        """CSIRO XML-based metadata to CKAN JSON map.

        **Args:**
            *uri*: the URI of the endpoint to connect and source CSIRO
            XML metadata

            *infile*: alternate file-based CSIRO XML metadata source file

        **Returns:**
            list of absolute paths to the file written

        """
        files_written = []

        self.loader.csiro_source_uri = uri
        self.loader.source(filename=infile)
        ckan_data = self.loader.translate()

        for guid, data in ckan_data.iteritems():
            files_written.append(self.dump_ckan_data(guid, data))

        return files_written

    def dump_ckan_data(self, guid, data):
        """Dump *data* structure to file.

        Targets :attr:`target_dir` as the base directory.  If not defined
        then the write will occur in the current directory.

        **Args:**
            *guid*: the unique ID of the CKAN record.  Used to build the
            output filename

            *data*: dictionary of GUID/data pairs.  For example::

                {
                    'DD006FCE-BEF5-4377-82AE-2C5A14B50E34': {
                        'default': 'test default value',
                        'contact_point': 'data.vsdl@depi.vic.gov.au',
                        'data_state': 'completed',
                        ...
                    }
                }

        **Returns:**
            list of files written.  For example::

                ['/target/DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json',
                 '/target/AAAAAAAA-BEF5-4377-82AE-2C5A14B50E34.json', ...]

        """
        target_path = guid + '.json'
        if self.target_dir is not None:
            target_path = os.path.join(self.target_dir, target_path)

        log.debug('Writing out GUID to target path "%s"' % target_path)
        target_fh = open(target_path, 'w')
        target_fh.write(json.dumps(data, indent=4))
        target_fh.close()

        return target_path
