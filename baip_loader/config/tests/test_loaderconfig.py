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
        cls.maxDiff = None
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

        received = self._conf.csiro_uri
        netloc = 'http://data.bioregionalassessments.gov.au'
        path = 'function/metadataexport'
        expected = '%s/%s' % (netloc, path)
        msg = 'LoaderConfig.csiro_path not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_url_scheme
        expected = 'http'
        msg = 'LoaderConfig.ckan_url_scheme not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_netloc
        expected = 'test.ddg.lws.links.com.au'
        msg = 'LoaderConfig.ckan_netloc not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_path
        expected = '/api/action/package_create'
        msg = 'LoaderConfig.ckan_netloc not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_uri
        expected = 'http://test.ddg.lws.links.com.au/api/action/package_create'
        msg = 'LoaderConfig.ckan_uri not as expected'
        self.assertEqual(received, expected, msg)

        received = self._conf.ckan_api_key
        expected = '524130fc-da5e-4d8c-b5c6-3e980b02f148'
        msg = 'LoaderConfig.ckan_api_key not as expected'
        self.assertEqual(received, expected, msg)

    def test_parse_config_ckan_mapper(self):
        """Parse items from the baip_loader.Config:ckan_mapper.
        """
        self._conf.set_config_file(self._file)
        self._conf.parse_config()
        received = self._conf.ckan_mapper
        expected = {'title': ['%s|%s|%s|%s|%s|%s' %
                              ('gmd:identificationInfo',
                               'gmd:MD_DataIdentification',
                               'gmd:citation',
                               'gmd:CI_Citation',
                               'gmd:title',
                               'gco:CharacterString')],
                    'tags': ['%s|%s|%s|%s' %
                             ('gmd:identificationInfo',
                              'gmd:MD_DataIdentification',
                              'gmd:topicCategory',
                              'gmd:MD_TopicCategoryCode'),
                             '%s|%s|%s|%s|%s|%s' %
                             ('gmd:identificationInfo',
                              'gmd:MD_DataIdentification',
                              'gmd:descriptiveKeywords',
                              'gmd:MD_Keywords',
                              'gmd:keyword',
                              'gco:CharacterString')]}
        msg = 'LoaderConfig.ckan_mapper not as expected'
        self.assertDictEqual(received, expected, msg)

    def test_parse_config_validation_sets(self):
        """Parse items from the baip_loader.Config:validation_sets.
        """
        # Given a defined list of geospatial topics
        vocab = ['Farming',
                 'Biota',
                 'Boundaries',
                 'Climatology Meteorology and Atmosphere',
                 'Economy',
                 'Elevation',
                 'Environment',
                 'Geoscientific information',
                 'Health',
                 'Imagery base maps and Earth cover',
                 'Intelligence and Military',
                 'Inland waters',
                 'Location',
                 'Oceans',
                 'Planning and Cadastre',
                 'Society',
                 'Transportation',
                 'Utilities and Communication']

        # when I enter the list into the geospatial_topic configuration
        # option
        self._conf.set_config_file(self._file)
        self._conf.parse_config()
        received = self._conf.validation_sets

        # then the values should be available to the baip_loader.Config
        # module
        expected = {'geospatial_topics': vocab}
        msg = 'baip_loader.Config:validation_sets config error'
        self.assertDictEqual(received, expected, msg)

    def test_parse_config_ckan_defaults(self):
        """Parse items from the baip_loader.Config:ckan_defaults.
        """
        # Given a value for the owner_org default configuration option
        owner_org = 'c5766f7d-963a-4f30-915e-f1a6f1143301'

        # when I add the option under the ckan_defaults configuration
        # section
        self._conf.set_config_file(self._file)
        self._conf.parse_config()
        received = self._conf.ckan_defaults

        # then the owner_org values should be available to the
        # baip_loader.Config module
        expected = {'owner_org': owner_org}
        msg = 'baip_loader.Config:ckan_defaults config error'
        self.assertDictEqual(received, expected, msg)

    def tearDown(self):
        self._conf = None
        del self._conf

    @classmethod
    def tearDownClass(cls):
        cls._file = None
        del cls._file
