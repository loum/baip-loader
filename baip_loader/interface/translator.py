import baip_loader
from logga.log import log

__all__ = ['Translator']


class Translator(object):
    """:class:`baip_loader.Translator`

    """
    @staticmethod
    def translate(uri=None, infile=None, outfile=None):
        loader = baip_loader.Loader()

        loader.csiro_source_uri = uri
        loader.source(filename=infile)
        outfile = loader.dump_translated(filename=outfile)

        return outfile
