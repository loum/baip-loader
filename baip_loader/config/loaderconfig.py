# pylint: disable=R0902,R0903,R0904,C0111,W0142
"""The :class:`baip_loader.LoaderConfig` is the configuration parser for
the BAIP Loader facility.

"""
__all__ = ["LoaderConfig"]


from configa.config import Config
from configa.setter import set_scalar


class LoaderConfig(Config):
    """
    .. attribute:: inbound_dir

        Staging directory for the CKAN JSON ingest files

    .. attribute:: csiro_url_scheme

        The type of the CSIRO endpoint URL.  For example ``http``

    .. attribute:: csiro_netloc

        The URL's network location part (CSIRO endpoint)

    .. attribute:: csiro_path

        The URL hierarchical path (CSIRO endpoint)

    .. attribute:: csiro_query

        The URL query component (CSIRO endpoint)

    .. attribute:: csiro_api_key

    """
    _inbound_dir = None
    _csiro_url_scheme = None
    _csiro_netloc = None
    _csiro_path = None
    _csiro_query = None
    _ckan_api_key = None

    def __init__(self, config_file=None):
        """:class:`baip_loader.LoaderConfig` initialisation.

        """
        Config.__init__(self, config_file)

    @property
    def inbound_dir(self):
        return self._inbound_dir

    @set_scalar
    def set_inbound_dir(self, value):
        pass

    @property
    def csiro_url_scheme(self):
        return self._csiro_url_scheme

    @set_scalar
    def set_csiro_url_scheme(self, value):
        pass

    @property
    def csiro_netloc(self):
        return self._csiro_netloc

    @set_scalar
    def set_csiro_netloc(self, value):
        pass

    @property
    def csiro_path(self):
        return self._csiro_path

    @set_scalar
    def set_csiro_path(self, value):
        pass

    @property
    def csiro_query(self):
        return self._csiro_query

    @set_scalar
    def set_csiro_query(self, value):
        pass

    @property
    def ckan_api_key(self):
        return self._ckan_api_key

    @set_scalar
    def set_ckan_api_key(self, value):
        pass

    def parse_config(self):
        """Read config items from the configuration file.

        """
        Config.parse_config(self)

        kwargs = [{'section': 'ingest',
                   'option': 'inbound_dir'},
                  {'section': 'csiro',
                   'var': 'csiro_url_scheme',
                   'option': 'url_scheme'},
                  {'section': 'csiro',
                   'var': 'csiro_netloc',
                   'option': 'netloc'},
                  {'section': 'csiro',
                   'var': 'csiro_path',
                   'option': 'path'},
                  {'section': 'csiro',
                   'var': 'csiro_query',
                   'option': 'query'},
                  {'section': 'ckan',
                   'var': 'ckan_api_key',
                   'option': 'api_key'}]

        for kwarg in kwargs:
            self.parse_scalar_config(**kwarg)
