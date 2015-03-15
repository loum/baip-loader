import baip_loader
from logga.log import log

__all__ = ['Mapper']


class Mapper(object):
    """:class:`baip_loader.Mapper`

    """
    @staticmethod
    def xml_to_ckan_map(uri=None, infile=None, outfile=None):
        """CSIRO XML-based metadata to CKAN JSON map.

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
