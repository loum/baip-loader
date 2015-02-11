# pylint: disable=R0904,C0103,W0142,W0212
""":class:`baip_loader.TestLoader` tests.

"""
import unittest2
import urlparse

import baip_loader


class TestLoader(unittest2.TestCase):
    """:class:`baip_loader.Loader` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def test_init(self):
        """Initialise a baip_loader.Loader object.
        """
        loader = baip_loader.Loader()
        msg = 'Object is not a baip_loader.Loader'
        self.assertIsInstance(loader, baip_loader.Loader, msg)

    def test_source(self):
        """Source CSIRO data.
        """
        scheme = 'http'
        netloc = 'data.bioregionalassessments.gov.au'
        path = '/function/metadataexport/dd006fce-bef5-4377-82ae-2c5a14b50e34'
        source_uri = urlparse.urlunsplit((scheme, netloc, path, None, None))
        loader = baip_loader.Loader(source_uri)
        loader.source()
