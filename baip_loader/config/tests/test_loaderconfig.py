# pylint: disable=R0904,C0103
""":class:`baip_loader.LoaderConfig` tests.

"""
import unittest2
import os

import baip_loader


class TestLoaderConfig(unittest2.TestCase):
    """:class:`baip_loader.LoaderConfig` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls._file = os.path.join('baip_loader',
                                 'config',
                                 'tests',
                                 'files',
                                 'baip-loader.conf')

    def setUp(self):
        self._conf = baip_loader.LoaderConfig()

    def test_init(self):
        """Initialise a LoaderConfig object.
        """
        msg = 'Object is not a baip_loader.LoaderConfig'
        self.assertIsInstance(self._conf, baip_loader.LoaderConfig, msg)

    def test_parse_config(self):
        """Parse comms items from the config.
        """
        self._conf.set_config_file(self._file)
        self._conf.parse_config()

        received = self._conf.inbound_dir
        expected = '/var/tmp/baip-loader'
        msg = 'LoaderConfig.inbound_dir not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_api_key
        expected = '524130fc-da5e-4d8c-b5c6-3e980b02f148'
        msg = 'LoaderConfig.ckan_api_key not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.csiro_url_scheme
        expected = 'http'
        msg = 'LoaderConfig.csiro_url_scheme not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.csiro_netloc
        expected = 'data.bioregionalassessments.gov.au'
        msg = 'LoaderConfig.csiro_netloc not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.csiro_path
        expected = '/function/metadataexport'
        msg = 'LoaderConfig.csiro_netloc not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.csiro_query
        expected = 'query'
        msg = 'LoaderConfig.csiro_path not as expected'
        self.assertEqual(received, expected, msg)

    def tearDown(self):
        self._conf = None
        del self._conf

    @classmethod
    def tearDownClass(cls):
        cls._file = None
        del cls._file
