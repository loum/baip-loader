import urlparse

from configa.config import Config
from configa.setter import (set_scalar,
                            set_dict)

__all__ = ["LoaderConfig"]


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

    .. attribute:: ckan_url_scheme

        The type of the CKAN endpoint URL.  For example ``http``

    .. attribute:: ckan_netloc

        The URL's network location part (CKAN endpoint)

    .. attribute:: ckan_path

        The URL hierarchical path (CKAN endpoint)

    .. attribute:: ckan_api_key

        Used to authorise your connection against the API function

    .. attribute:: ckan_mapper

    .. attribute:: validation_sets

        Lists of vocabularies that are used to validate CKAN data

    """
    _inbound_dir = None
    _csiro_url_scheme = None
    _csiro_netloc = None
    _csiro_path = None
    _csiro_query = None
    _ckan_url_scheme = None
    _ckan_netloc = None
    _ckan_path = None
    _ckan_api_key = None
    _ckan_mapper = {}
    _validation_sets = {}

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
    def csiro_uri(self):
        scheme = self.csiro_url_scheme
        netloc = self.csiro_netloc
        path = self.csiro_path

        return urlparse.urlunsplit((scheme, netloc, path, None, None))

    @property
    def ckan_url_scheme(self):
        return self._ckan_url_scheme

    @set_scalar
    def set_ckan_url_scheme(self, value):
        pass

    @property
    def ckan_netloc(self):
        return self._ckan_netloc

    @set_scalar
    def set_ckan_netloc(self, value):
        pass

    @property
    def ckan_path(self):
        return self._ckan_path

    @set_scalar
    def set_ckan_path(self, value):
        pass

    @property
    def ckan_uri(self):
        scheme = self.ckan_url_scheme
        netloc = self.ckan_netloc
        path = self.ckan_path

        return urlparse.urlunsplit((scheme, netloc, path, None, None))

    @property
    def ckan_api_key(self):
        return self._ckan_api_key

    @set_scalar
    def set_ckan_api_key(self, value):
        pass

    @property
    def ckan_mapper(self):
        return self._ckan_mapper

    @set_dict
    def set_ckan_mapper(self, values=None):
        pass

    @property
    def validation_sets(self):
        return self._validation_sets

    @set_dict
    def set_validation_sets(self, values=None):
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
                   'var': 'ckan_url_scheme',
                   'option': 'url_scheme'},
                  {'section': 'ckan',
                   'var': 'ckan_netloc',
                   'option': 'netloc'},
                  {'section': 'ckan',
                   'var': 'ckan_path',
                   'option': 'path'},
                  {'section': 'ckan_header',
                   'var': 'ckan_api_key',
                   'option': 'api_key'}]

        for kwarg in kwargs:
            self.parse_scalar_config(**kwarg)

        del kwargs[:]
        kwargs = [{'section': 'ckan_mapper',
                   'is_list': True},
                  {'section': 'validation_sets',
                   'is_list': True}]
        for kwarg in kwargs:
            self.parse_dict_config(**kwarg)
