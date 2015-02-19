import baip_loader
from logga.log import log

__all__ = ['Translator']


class Translator(object):
    """:class:`baip_loader.Translator`

    """
    @staticmethod
    def translate(uri=None, infile=None, outfile=None):
        """CSIRO XML-based metadata to JSON converter.

        **Args:**
            *uri*: the URI of the endpoint to connect and source CSIRO
            XML metadata

            *infile*: alternate file-based CSIRO XML metadata

            *outfile*: specify the name of the output file to use

        **Returns:**
            the absolute path to the output file written

        """
        loader = baip_loader.Loader()

        loader.csiro_source_uri = uri
        loader.source(filename=infile)
        outfile = loader.dump_translated(filename=outfile)

        return outfile
