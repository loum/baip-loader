import unittest2
import os
import json

import baip_loader
from baip_loader.tests.files.iso19115_single_record import ISO19115_ITEM
from baip_loader.tests.files.iso19115_single_record_url import ISO19115_ITEM_URL
from baip_loader.tests.files.iso19115_single_record_temporal import ISO19115_ITEM_TEMPORAL
from baip_loader.tests.results.iso19115_to_ckan_map_all_fields import MAP_ALL_FIELDS
from baip_loader.tests.results.ckan_sanitised import SANITISED_CKAN
from baip_loader.tests.results.ckan_reformatted import REFORMATTED_CKAN
from baip_loader.tests.results.ckan_defaults import DEFAULTS_CKAN


class TestLoader(unittest2.TestCase):
    """:class:`baip_loader.Loader` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls._source_dir = os.path.join('baip_loader', 'tests', 'files')
        cls._results_dir = os.path.join('baip_loader', 'tests', 'results')

    def test_init(self):
        """Initialise a baip_loader.Loader object.
        """
        loader = baip_loader.Loader()
        msg = 'Object is not a baip_loader.Loader'
        self.assertIsInstance(loader, baip_loader.Loader, msg)

    def test_source_from_filename(self):
        """Source data: filename.
        """
        loader = baip_loader.Loader()
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record.xml')

        loader.source(source_xml_file)
        received = loader.csiro_source_data
        source_xml_obj = open(source_xml_file)
        expected = source_xml_obj.read()
        source_xml_obj.close()
        msg = 'XML source contents are different'
        self.assertEqual(received, expected, msg)

    def test_xml2json(self):
        """XML to JSON conversion.
        """
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record.xml')
        source_xml_obj = open(source_xml_file)

        received = baip_loader.Loader.xml2json(source_xml_obj.read())
        target_json_file = os.path.join(self._results_dir,
                                        'baip-meta-single-record.json')
        target_json_obj = open(target_json_file)
        expected = target_json_obj.read().strip()
        msg = 'XML to JSON output is different'
        self.assertEqual(received, expected, msg)

        # Clean up.
        source_xml_obj.close()
        target_json_obj.close()

    def test_translate(self):
        """XML to JSON translate.
        """
        # Given a CSIRO BAIP XML metadata structure
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-multiple-records.xml')
        loader = baip_loader.Loader()
        loader.source(filename=source_xml_file)

        # and a simple CKAN mapper definition
        levels = {'title': ['%s|%s|%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:citation',
                             'gmd:CI_Citation',
                             'gmd:title',
                             'gco:CharacterString')]}
        loader.ckan_mapper = levels

        # and a simple defaults definition
        defaults = {'test': 'default'}
        loader.ckan_defaults = defaults

        # when I map to CKAN data.gov.au JSON structure
        received = loader.translate()

        # then the CSIRO XML input should translated to a CKAN data map
        # of the form {<guid>: <ckan_ingest_data>}
        expected = {
            '6968B11F-9912-42CA-8536-00CDE75E75D9': {
                'test': 'default',
                'title': u'Asset list for Galilee - CURRENT'
            },
            '457ED79A-C6DF-4AAF-A480-00926E48CAA8': {
                'test': 'default',
                'title': u'CLM - Logan-Albert catchment boundary'
            },
            '6151C409-0CAF-4727-9F57-00F6B71A58FB': {
                'test': 'default',
                'title': u'Layer 05-07 Great Artesian Basin base of Algebuckina Sandstone surface (GABWRA)'
            },
            '781A8B81-93B8-4CDE-9B56-00291D7543EA': {
                'test': 'default',
                'title': u'GLO Catchments Water Source Boundaries'
            }
        }
        msg = 'Translated CKAN data error'
        self.assertDictEqual(received, expected, msg)

    def test_extract_multiple_guids(self):
        """Extract multiple GUID.
        """
        # Given a JSON data structure with multiple items
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-multiple-records.xml')

        # when I want to extract the GUIDs
        loader = baip_loader.Loader()
        loader.source(filename=source_xml_file)
        received = loader.extract_guids()

        # then a list of GUIDs is to be returned
        expected = [(u'781A8B81-93B8-4CDE-9B56-00291D7543EA', None),
                    (u'457ED79A-C6DF-4AAF-A480-00926E48CAA8', None),
                    (u'6968B11F-9912-42CA-8536-00CDE75E75D9', None),
                    (u'6151C409-0CAF-4727-9F57-00F6B71A58FB', None)]
        msg = 'list of GUIDs incorrect'
        self.assertListEqual(list(received), expected, msg)

    def test_extract_single_guid(self):
        """Extract single GUID.
        """
        # Given a JSON data structure with multiple items
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record.xml')

        # when I want to extract the GUIDs
        loader = baip_loader.Loader()
        loader.source(filename=source_xml_file)
        received = loader.extract_guids()

        # then a list of GUIDs is to be returned
        expected = [(u'DD006FCE-BEF5-4377-82AE-2C5A14B50E34', None)]
        msg = 'list of GUIDs incorrect'
        self.assertListEqual(list(received), expected, msg)

    def test_extract_guid(self):
        """Extract the GUID from the CSIRO dictionary structure.
        """
        source_dict = {
            'gmd:MD_Metadata': {
                'gmd:fileIdentifier': {
                    'gco:CharacterString':
                        'DD006FCE-BEF5-4377-82AE-2C5A14B50E34'
                }
            }
        }

        sample_data = source_dict['gmd:MD_Metadata']
        received = baip_loader.Loader.extract_guid(sample_data)
        expected = 'DD006FCE-BEF5-4377-82AE-2C5A14B50E34'
        msg = 'Extracted GUID error'
        self.assertEqual(received, expected, msg)

    def test_prepare_json_item(self):
        """
        """
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record-small.xml')
        source_xml_obj = open(source_xml_file)
        source_xml = source_xml_obj.read()
        source_xml_obj.close()

        loader = baip_loader.Loader()
        received = loader.extract_guids(source_xml,
                                        to_json=True)
        expected = [(u'DD006FCE-BEF5-4377-82AE-2C5A14B50E34', '{"@xmlns:gmd": "http://www.isotc211.org/2005/gmd", "gmd:fileIdentifier": {"gco:CharacterString": "DD006FCE-BEF5-4377-82AE-2C5A14B50E34"}}')]
        msg = 'Extracted GUID error'
        self.assertListEqual(list(received), expected, msg)

    def test_extract_iso19115_field_valid_dictionary(self):
        """ISO19115 field extraction: valid dictionary
        """
        # Given an ISO19115 XML data structure
        xml_data = ISO19115_ITEM

        # when I perform a mapping request
        levels = ['gmd:identificationInfo',
                  'gmd:MD_DataIdentification',
                  'gmd:citation',
                  'gmd:CI_Citation',
                  'gmd:title',
                  'gco:CharacterString']
        received = baip_loader.Loader.extract_iso19115_field(levels,
                                                             xml_data)

        # then the MD_Metadata.identificationInfo:MD_DataIdentification.\
        # citation:CI_Citation.title field should be extracted
        expected = 'Victorian Aquifer Framework - Salinity'
        msg = 'ISO19115 extract error'
        self.assertEqual(received, expected, msg)

    def test_extract_iso19115_field_empty_dictionary(self):
        """ISO19115 field extraction: valid dictionary
        """
        # Given an empty dictionary
        xml_data = {}

        # when I perform a mapping request
        levels = ['gmd:identificationInfo',
                  'gmd:MD_DataIdentification',
                  'gmd:citation',
                  'gmd:CI_Citation',
                  'gmd:title',
                  'gco:CharacterString']
        received = baip_loader.Loader.extract_iso19115_field(levels,
                                                             xml_data)

        # then no dadta should be extracted
        msg = 'ISO19115 extract from empty dictionary error'
        self.assertIsNone(received, msg)

    def test_extract_iso19115_field_bad_level(self):
        """ISO19115 field extraction: bad level.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when I perform a mapping request
        levels = ['gmd:identificationInfo',
                  'gmd:MD_DataIdentification',
                  'gmd:citation',
                  'gmd:CI_Citation',
                  'gmd:title',
                  'gco:banana']
        received = baip_loader.Loader.extract_iso19115_field(levels,
                                                             xml_data)

        # then no data should be extracted
        msg = 'ISO19115 extract from empty dictionary error'
        self.assertIsNone(received, msg)

    def test_extract_iso19115_field_level_as_list(self):
        """ISO19115 field extraction: level as list.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when I source levels that feature a nested list
        levels = ['gmd:identificationInfo',
                  'gmd:MD_DataIdentification',
                  'gmd:descriptiveKeywords',
                  'gmd:MD_Keywords',
                  'gmd:keyword',
                  'gco:CharacterString']

        # and I perform a mapping request
        received = baip_loader.Loader.extract_iso19115_field(levels,
                                                             xml_data)

        # then data should be extracted
        expected = [u'Victoria']
        msg = 'ISO19115 extract from dictionary with nested list error'
        self.assertListEqual(received, expected, msg)

    def test_iso19115_to_ckan_map(self):
        """CSIRO ISO19115 to CKAN map.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ANZLIC map source fields are defined
        levels = {'title': ['%s|%s|%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:citation',
                             'gmd:CI_Citation',
                             'gmd:title',
                             'gco:CharacterString')],
                  'notes': ['%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:abstract',
                             'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)
        # Truncate the long notes ...
        received['notes'][0] = received['notes'][0][:30] + '...'

        # then CKAN data should be extracted
        expected = {'title': [u'Victorian Aquifer Framework - Salinity'],
                    'notes': [u'[This data and its metadata st...']}
        msg = 'ISO19115 to CKAN map error'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_multi_source(self):
        """CSIRO ISO19115 to CKAN map: multi-source.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ANZLIC map column features multiple sources fields
        levels = {'tags': ['%s|%s|%s|%s' %
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

        # when I perform a keyword mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # then CKAN data should be extracted
        expected = {'tags': [u'inlandWaters', [u'Victoria']]}
        msg = 'ISO19115 to CKAN map error'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_language(self):
        """CSIRO ISO19115 to CKAN map: language.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper language field is mapped to the
        # MD_Metadata.identificationInfo:MD_DataIdentification.language
        # ISO19115 element
        levels = {'language': ['%s|%s|%s|%s' %
                               ('gmd:identificationInfo',
                                'gmd:MD_DataIdentification',
                                'gmd:language',
                                'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'language': [u'eng']}
        msg = 'ISO19115 to CKAN map error: language'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_licence(self):
        """CSIRO ISO19115 to CKAN map: licence.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper language field is mapped to the
        # MD_LegalConstraints ISO19115 element
        levels = {'licence': ['%s|%s|%s|%s|%s|%s' %
                              ('gmd:identificationInfo',
                               'gmd:MD_DataIdentification',
                               'gmd:resourceConstraints',
                               'gmd:MD_LegalConstraints',
                               'gmd:useLimitation',
                               'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        json_fh = open(os.path.join(self._results_dir,
                                    'iso19115-ckan-mapper-licence.json'))
        expected = json.load(json_fh)
        msg = 'ISO19115 to CKAN map error: licence'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_update_frequency(self):
        """CSIRO ISO19115 to CKAN map: update_frequency.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper update_frequency field is mapped to the
        # MD_LegalConstraints ISO19115 element
        levels = {'update_frequency': ['%s|%s|%s|%s|%s|%s|%s' %
                                       ('gmd:identificationInfo',
                                        'gmd:MD_DataIdentification',
                                        'gmd:resourceMaintenance',
                                        'gmd:MD_MaintenanceInformation',
                                        'gmd:maintenanceAndUpdateFrequency',
                                        'gmd:MD_MaintenanceFrequencyCode',
                                        '#text')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'update_frequency': [u'asNeeded']}
        msg = 'ISO19115 to CKAN map error: update_frequency'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_dates(self):
        """CSIRO ISO19115 to CKAN map: dates.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper update_frequency field is mapped to the
        # MD_LegalConstraints ISO19115 element
        levels = {'dates': ['%s|%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:citation',
                             'gmd:CI_Citation',
                             'gmd:date')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        json_fh = open(os.path.join(self._results_dir,
                                    'iso19115-ckan-mapper-dates.json'))
        expected = json.load(json_fh)
        msg = 'ISO19115 to CKAN map error: dates'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_id(self):
        """CSIRO ISO19115 to CKAN map: id.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper update_frequency field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'id': ['%s|%s' % ('gmd:fileIdentifier',
                                    'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'id': [u'DD006FCE-BEF5-4377-82AE-2C5A14B50E34']}
        msg = 'ISO19115 to CKAN map error: id'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_url(self):
        """CSIRO ISO19115 to CKAN map: download_url.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_URL

        # when the ckan_mapper download_url field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'download_url': ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' %
                                   ('gmd:distributionInfo',
                                    'gmd:MD_Distribution',
                                    'gmd:distributor',
                                    'gmd:MD_Distributor',
                                    'gmd:distributorTransferOptions',
                                    'gmd:MD_DigitalTransferOptions',
                                    'gmd:onLine',
                                    'gmd:CI_OnlineResource',
                                       'gmd:linkage',
                                       'gmd:URL')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'download_url': [u'n/a']}
        msg = 'ISO19115 to CKAN map error: download_url'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_url_missing(self):
        """CSIRO ISO19115 to CKAN map: download_url missing.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'download_url': ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' %
                                   ('gmd:distributionInfo',
                                    'gmd:MD_Distribution',
                                    'gmd:distributor',
                                    'gmd:MD_Distributor',
                                    'gmd:distributorTransferOptions',
                                    'gmd:MD_DigitalTransferOptions',
                                    'gmd:onLine',
                                    'gmd:CI_OnlineResource',
                                    'gmd:linkage',
                                    'gmd:URL')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'download_url': [None]}
        msg = 'ISO19115 to CKAN map error: download_url missing'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_file_size(self):
        """CSIRO ISO19115 to CKAN map: file_size.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_URL

        # when the ckan_mapper download_url field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'file_size': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                ('gmd:distributionInfo',
                                 'gmd:MD_Distribution',
                                 'gmd:distributor',
                                 'gmd:MD_Distributor',
                                 'gmd:distributorTransferOptions',
                                 'gmd:MD_DigitalTransferOptions',
                                 'gmd:transferSize',
                                 'gco:Real')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'file_size': [u'0.00']}
        msg = 'ISO19115 to CKAN map error: file_size'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_file_size_missing(self):
        """CSIRO ISO19115 to CKAN map: file_size missing.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'file_size': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                ('gmd:distributionInfo',
                                 'gmd:MD_Distribution',
                                 'gmd:distributor',
                                 'gmd:MD_Distributor',
                                 'gmd:distributorTransferOptions',
                                 'gmd:MD_DigitalTransferOptions',
                                 'gmd:transferSize',
                                 'gco:Real')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'file_size': [None]}
        msg = 'ISO19115 to CKAN map error: file_size missing'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_publisher(self):
        """CSIRO ISO19115 to CKAN map: publisher.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # MD_Metadata.fileIdentifier ISO19115 element
        levels = {'publisher': ['%s|%s|%s|%s' %
                                ('gmd:contact',
                                 'gmd:CI_ResponsibleParty',
                                 'gmd:organisationName',
                                 'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {
            'publisher': [
                u'VIC - Department of Environment and Primary Industries'
            ]
        }
        msg = 'ISO19115 to CKAN map error: publisher'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_jurisdiction(self):
        """CSIRO ISO19115 to CKAN map: jurisdiction.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_URL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_GeographicDescription ISO19115 element
        levels = {'jurisdiction': ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' %
                                   ('gmd:identificationInfo',
                                    'gmd:MD_DataIdentification',
                                    'gmd:extent',
                                    'gmd:EX_Extent',
                                    'gmd:geographicElement',
                                    'gmd:EX_GeographicDescription',
                                    'gmd:geographicIdentifier',
                                    'gmd:MD_Identifier',
                                    'gmd:code',
                                    'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'jurisdiction': [['NSW']]}
        msg = 'ISO19115 to CKAN map error: jurisdiction'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_jurisdiction_missing(self):
        """CSIRO ISO19115 to CKAN map: jurisdiction missing.
        """
        # Given a dictionary with missing jurisdiction
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_GeographicDescription ISO19115 element
        levels = {'jurisdiction': ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' %
                                   ('gmd:identificationInfo',
                                    'gmd:MD_DataIdentification',
                                    'gmd:extent',
                                    'gmd:EX_Extent',
                                    'gmd:geographicElement',
                                    'gmd:EX_GeographicDescription',
                                    'gmd:geographicIdentifier',
                                    'gmd:MD_Identifier',
                                    'gmd:code',
                                    'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'jurisdiction': [None]}
        msg = 'ISO19115 to CKAN map error: jurisdiction missing'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_temporal_coverage_from(self):
        """CSIRO ISO19115 to CKAN map: temporal_coverage_from.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {
            'temporal_coverage_from': [
                '%s|%s|%s|%s|%s|%s|%s|%s|%s' % ('gmd:identificationInfo',
                                                'gmd:MD_DataIdentification',
                                                'gmd:extent',
                                                'gmd:EX_Extent',
                                                'gmd:temporalElement',
                                                'gmd:EX_TemporalExtent',
                                                'gmd:extent',
                                                'gml:TimePeriod',
                                                'gml:beginPosition')
            ]
        }

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'temporal_coverage_from': [['2000-04-01T00:04:00']]}
        msg = 'ISO19115 to CKAN map error: temporal_coverage_from'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_temporal_coverage_from_missing(self):
        """CSIRO ISO19115 to CKAN map: temporal_coverage_from missing.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {
            'temporal_coverage_from': [
                '%s|%s|%s|%s|%s|%s|%s|%s|%s' % ('gmd:identificationInfo',
                                                'gmd:MD_DataIdentification',
                                                'gmd:extent',
                                                'gmd:EX_Extent',
                                                'gmd:temporalElement',
                                                'gmd:EX_TemporalExtent',
                                                'gmd:extent',
                                                'gml:TimePeriod',
                                                'gml:beginPosition')
            ]
        }

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'temporal_coverage_from': [None]}
        msg = 'ISO19115 to CKAN map error: temporal_coverage_from missing'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_temporal_coverage_to(self):
        """CSIRO ISO19115 to CKAN map: temporal_coverage_to.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {
            'temporal_coverage_from': [
                '%s|%s|%s|%s|%s|%s|%s|%s|%s' % ('gmd:identificationInfo',
                                                'gmd:MD_DataIdentification',
                                                'gmd:extent',
                                                'gmd:EX_Extent',
                                                'gmd:temporalElement',
                                                'gmd:EX_TemporalExtent',
                                                'gmd:extent',
                                                'gml:TimePeriod',
                                                'gml:endPosition')
            ]
        }

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'temporal_coverage_from': [['2008-04-01T23:04:00']]}
        msg = 'ISO19115 to CKAN map error: temporal_coverage_to'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_download_temporal_coverage_to_missing(self):
        """CSIRO ISO19115 to CKAN map: temporal_coverage_to missing.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {
            'temporal_coverage_from': [
                '%s|%s|%s|%s|%s|%s|%s|%s|%s' % ('gmd:identificationInfo',
                                                'gmd:MD_DataIdentification',
                                                'gmd:extent',
                                                'gmd:EX_Extent',
                                                'gmd:temporalElement',
                                                'gmd:EX_TemporalExtent',
                                                'gmd:extent',
                                                'gml:TimePeriod',
                                                'gml:endPosition')
            ]
        }

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'temporal_coverage_from': [None]}
        msg = 'ISO19115 to CKAN map error: temporal_coverage_to missing'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_spatial_coverage_polygon(self):
        """CSIRO ISO19115 to CKAN map: spatial_coverage - polygon.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'polygon': ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' %
                              ('gmd:identificationInfo',
                               'gmd:MD_DataIdentification',
                               'gmd:extent',
                               'gmd:EX_Extent',
                               'gmd:geographicElement',
                               'gmd:EX_BoundingPolygon',
                               'gmd:polygon',
                               'gml:Polygon',
                               'gml:exterior',
                               'gml:LinearRing',
                               'gml:pos')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'polygon': [[['110.0012 -10.00117',
                                  '115.008 -10.00117',
                                  '155.008 -45.00362',
                                  '110.0012 -45.00362',
                                  '110.0012 -10.00117']]]}
        msg = 'ISO19115 to CKAN map error: spatial polygon'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_spatial_coverage_bbox_west(self):
        """CSIRO ISO19115 to CKAN map: spatial_coverage - bbox west.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'bbox_west': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                ('gmd:identificationInfo',
                                 'gmd:MD_DataIdentification',
                                 'gmd:extent',
                                 'gmd:EX_Extent',
                                 'gmd:geographicElement',
                                 'gmd:EX_GeographicBoundingBox',
                                 'gmd:westBoundLongitude',
                                 'gco:Decimal')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'bbox_west': [['110.0012']]}
        msg = 'ISO19115 to CKAN map error: spatial bbox:west'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_spatial_coverage_bbox_east(self):
        """CSIRO ISO19115 to CKAN map: spatial_coverage - bbox east.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'bbox_east': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                ('gmd:identificationInfo',
                                 'gmd:MD_DataIdentification',
                                 'gmd:extent',
                                 'gmd:EX_Extent',
                                 'gmd:geographicElement',
                                 'gmd:EX_GeographicBoundingBox',
                                 'gmd:eastBoundLongitude',
                                 'gco:Decimal')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'bbox_east': [['155.008']]}
        msg = 'ISO19115 to CKAN map error: spatial bbox:east'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_spatial_coverage_bbox_north(self):
        """CSIRO ISO19115 to CKAN map: spatial_coverage - bbox north.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'bbox_north': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                 ('gmd:identificationInfo',
                                  'gmd:MD_DataIdentification',
                                  'gmd:extent',
                                  'gmd:EX_Extent',
                                  'gmd:geographicElement',
                                  'gmd:EX_GeographicBoundingBox',
                                  'gmd:northBoundLatitude',
                                  'gco:Decimal')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'bbox_north': [['-10.00117']]}
        msg = 'ISO19115 to CKAN map error: spatial bbox:east'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_spatial_coverage_bbox_south(self):
        """CSIRO ISO19115 to CKAN map: spatial_coverage - bbox south.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'bbox_south': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                 ('gmd:identificationInfo',
                                  'gmd:MD_DataIdentification',
                                  'gmd:extent',
                                  'gmd:EX_Extent',
                                  'gmd:geographicElement',
                                  'gmd:EX_GeographicBoundingBox',
                                  'gmd:southBoundLatitude',
                                  'gco:Decimal')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'bbox_south': [['-45.00362']]}
        msg = 'ISO19115 to CKAN map error: spatial bbox:south'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_topic(self):
        """CSIRO ISO19115 to CKAN map: topic.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'geospatial_topic': ['%s|%s|%s|%s' %
                                       ('gmd:identificationInfo',
                                        'gmd:MD_DataIdentification',
                                        'gmd:topicCategory',
                                        'gmd:MD_TopicCategoryCode')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'geospatial_topic': ['environment']}
        msg = 'ISO19115 to CKAN map error: topic'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_field_of_research(self):
        """CSIRO ISO19115 to CKAN map: field_of_research.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper download_url field is mapped to the
        # ...:EX_Extent.temporalElement ISO19115 element
        levels = {'field_of_research': ['%s|%s|%s|%s|%s|%s' %
                                        ('gmd:identificationInfo',
                                         'gmd:MD_DataIdentification',
                                         'gmd:descriptiveKeywords',
                                         'gmd:MD_Keywords',
                                         'gmd:keyword',
                                         'gco:CharacterString'),
                                        '%s|%s|%s|%s|%s|%s|%s|%s' %
                                         ('gmd:identificationInfo',
                                          'gmd:MD_DataIdentification',
                                          'gmd:descriptiveKeywords',
                                          'gmd:MD_Keywords',
                                          'gmd:thesaurusName',
                                          'gmd:CI_Citation',
                                          'gmd:title',
                                          'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'field_of_research': [['Australia'],
                                          ['ANZLIC Jurisdictions']]}
        msg = 'ISO19115 to CKAN map error: field_of_research'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_organization_title(self):
        """CSIRO ISO19115 to CKAN map: organization[title].
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM_TEMPORAL

        # when the ckan_mapper organization|title field is mapped to the
        # ...:gmd:CI_ResponsibleParty|gmd:organisationName
        # ISO19115 element
        levels = {'organization|title': ['%s|%s|%s|%s' %
                                         ('gmd:contact',
                                          'gmd:CI_ResponsibleParty',
                                          'gmd:organisationName',
                                          'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {
            'organization|title': [
                'Geoscience Australia'
            ]
        }
        msg = 'ISO19115 to CKAN map error: organization|title'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_extras_telephone(self):
        """CSIRO ISO19115 to CKAN map: extras[telephone].
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper organization|title field is mapped to the
        # ...:gmd:CI_ResponsibleParty|gmd:organisationName
        # ISO19115 element
        levels = {'extras|telephone': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                       ('gmd:contact',
                                        'gmd:CI_ResponsibleParty',
                                        'gmd:contactInfo',
                                        'gmd:CI_Contact',
                                        'gmd:phone',
                                        'gmd:CI_Telephone',
                                        'gmd:voice',
                                        'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'extras|telephone': ['86362385']}
        msg = 'ISO19115 to CKAN map error: organization|title'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_contact_point(self):
        """CSIRO ISO19115 to CKAN map: contact_point.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper contact_point field is mapped to the
        # ...:gmd:CI_ResponsibleParty|gmd:organisationName
        # ISO19115 element
        levels = {'contact_point': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                    ('gmd:contact',
                                     'gmd:CI_ResponsibleParty',
                                     'gmd:contactInfo',
                                     'gmd:CI_Contact',
                                     'gmd:address',
                                     'gmd:CI_Address',
                                     'gmd:electronicMailAddress',
                                     'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'contact_point': ['data.vsdl@depi.vic.gov.au']}
        msg = 'ISO19115 to CKAN map error: contact_point'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_metadata_modified(self):
        """CSIRO ISO19115 to CKAN map: metadata_modified.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper contact_point field is mapped to the
        # ...dateStamp.Date
        # ISO19115 element
        levels = {'metadata_modified': ['%s|%s' % ('gmd:dateStamp',
                                                   'gco:Date')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'metadata_modified': ['2015-02-10']}
        msg = 'ISO19115 to CKAN map error: metadata_modified'
        self.assertDictEqual(received, expected, msg)

    def test_extract_iso19115_dates(self):
        """Extract ISO19115 XML dates.
        """
        # Given a ISO19115 dates based dictionary
        json_dates_fh = open(os.path.join(self._results_dir,
                                          'iso19115-ckan-mapper-dates.json'))
        iso19115_dates = json.load(json_dates_fh)

        # when I extract the "creation", "publication" and "revision" dates
        dates = iso19115_dates.get('dates')
        received = baip_loader.Loader.extract_iso19115_dates(dates)

        # then I should receive a dictionary of the form
        # {<date_type>, <ISO_8660_date>, ...}
        expected = {'publication': '2014-10-24',
                    'revision': '2015-02-10',
                    'creation': '2015-02-10'}
        msg = 'ISO19115 dates extraction error'
        self.assertDictEqual(received, expected, msg)

    def test_ckan_map(self):
        """Map an ISO19115 record to a CKAN dictionary data structure.
        """
        # Given an ISO19115 XML data structure
        xml_data = ISO19115_ITEM_TEMPORAL

        # and a CKAN mapping rule set in the configuration file
        conf_file = os.path.join('baip_loader', 'conf', 'loader.conf')
        conf = baip_loader.LoaderConfig(conf_file)
        conf.parse_config()

        # when I map the ckan_mapper fields to an ISO19115 record
        loader = baip_loader.Loader()
        loader.ckan_mapper = conf.ckan_mapper
        received = loader.iso19115_to_ckan_map(xml_data)

        # the ISO19115 values should be mapped to the CKAN ingest
        # data structure
        expected = MAP_ALL_FIELDS
        msg = 'ISO19115 dates extraction error'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_revision_id(self):
        """CSIRO ISO19115 to CKAN map: revision_id.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper contact_point field is mapped to the
        # ...gmd:CI_Citation.gmd:edition
        # ISO19115 element
        levels = {'revision_id': ['%s|%s|%s|%s|%s|%s|%s|%s' %
                                  ('gmd:identificationInfo',
                                   'gmd:MD_DataIdentification',
                                   'gmd:descriptiveKeywords',
                                   'gmd:MD_Keywords',
                                   'gmd:thesaurusName',
                                   'gmd:CI_Citation',
                                   'gmd:edition',
                                   'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'revision_id': [['Version 2.1']]}
        msg = 'ISO19115 to CKAN map error: revision_id'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_notes(self):
        """CSIRO ISO19115 to CKAN map: notes.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper contact_point field is mapped to the
        # ...gmd:MD_DataIdentification.gmd:abstract
        # ISO19115 element
        levels = {'notes': ['%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:abstract',
                             'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)
        received['notes'][0] = received['notes'][0][:30] + '...'

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'notes': ['[This data and its metadata st...']}
        msg = 'ISO19115 to CKAN map error: notes'
        self.assertDictEqual(received, expected, msg)

    def test_iso19115_to_ckan_map_data_state(self):
        """CSIRO ISO19115 to CKAN map: data_state.
        """
        # Given a dictionary
        xml_data = ISO19115_ITEM

        # when the ckan_mapper contact_point field is mapped to the
        # ...gmd:status.gmd:MD_ProgressCode.#text
        # ISO19115 element
        levels = {'data_state': ['%s|%s|%s|%s|%s' %
                                 ('gmd:identificationInfo',
                                  'gmd:MD_DataIdentification',
                                  'gmd:status',
                                  'gmd:MD_ProgressCode',
                                  '#text')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)

        # the the element value should be mapped to the JSON ingest data
        # structure
        expected = {'data_state': ['completed']}
        msg = 'ISO19115 to CKAN map error: data_state'
        self.assertDictEqual(received, expected, msg)

    def test_sanitise(self):
        """Sanitise CKAN-ready data structure.
        """
        # Given an extracted CKAN data structure
        data = MAP_ALL_FIELDS

        # when I sanitise the data
        loader = baip_loader.Loader()
        received = loader.sanitise(data)

        # then the data values should be converted to a format that can
        # be ingest into CKAN
        expected = SANITISED_CKAN
        msg = 'CKAN sanitisation error'
        self.assertDictEqual(received, expected, msg)

    def test_extract_iso19115_spatial_with_polygon(self):
        """Extract ISO19115 spatial: polygon.
        """
        # Given an ISO19115 XML spatial data structure
        data = {
            'bbox_east': [['155.008']],
            'bbox_north': [['-10.00117']],
            'bbox_south': [['-45.00362']],
            'bbox_west': [['110.0012']],
            'polygon': [
                [
                    [
                        '110.0012 -10.00117',
                        '115.008 -10.00117',
                        '155.008 -45.00362',
                        '110.0012 -45.00362',
                        '110.0012 -10.00117'
                    ]
                ]
            ]
        }

        # when I extract the CKAN spatial component
        received = baip_loader.Loader.extract_iso19115_spatial(data)

        # then I should receive a dictionary of the form
        # {'spatial_coverage': <spatial content>}
        expected = {
            'spatial': [
                [
                    '155.008', '-10.00117', '-45.00362', '110.0012'
                ],
            ],
            'spatial_coverage': [
                [
                    [
                        '110.0012 -10.00117',
                        '115.008 -10.00117',
                        '155.008 -45.00362',
                        '110.0012 -45.00362',
                        '110.0012 -10.00117'
                    ]
                ]
            ]
        }
        msg = 'ISO19115 spatial extraction error: polygon'
        self.assertDictEqual(received, expected, msg)

    def test_extract_iso19115_spatial_with_bbox(self):
        """Extract ISO19115 spatial: bbox.
        """
        # Given an ISO19115 XML spatial data structure
        data = {
            'bbox_east': [['155.008']],
            'bbox_north': [['-10.00117']],
            'bbox_south': [['-45.00362']],
            'bbox_west': [['110.0012']],
            'polygon': [[[]]]
        }

        # when I extract the CKAN spatial component
        received = baip_loader.Loader.extract_iso19115_spatial(data)

        # then I should receive a dictionary of the form
        # {'spatial_coverage': <spatial content>}
        expected = {
            'spatial': [
                [
                    '155.008', '-10.00117', '-45.00362', '110.0012'
                ],
            ],
            'spatial_coverage': [
                [
                    '155.008', '-10.00117', '-45.00362', '110.0012',
                ],
            ]
        }
        msg = 'ISO19115 spatial extraction error: bbox'
        self.assertDictEqual(received, expected, msg)

    def test_extract_iso19115_spatial_with_no_spatial(self):
        """Extract ISO19115 spatial: no spatial.
        """
        # Given an ISO19115 XML spatial data structure
        data = {
            'bbox_east': [[]],
            'bbox_north': [[]],
            'bbox_south': [[]],
            'bbox_west': [[]],
            'polygon': [[[]]]
        }

        # when I extract the CKAN spatial component
        received = baip_loader.Loader.extract_iso19115_spatial(data)

        # then I should receive a dictionary of the form
        # {'spatial_coverage': <spatial content>}
        expected = {}
        msg = 'ISO19115 spatial extraction error: no spatial'
        self.assertDictEqual(received, expected, msg)

    def test_reformat(self):
        """Re-format CKAN sanitised data structure.
        """
        # Given an extracted CKAN data structure
        data = SANITISED_CKAN

        # when I reformat the data
        received = baip_loader.Loader.reformat(data)

        # then the data values should be converted to a format that can
        # be ingest into CKAN
        expected = REFORMATTED_CKAN
        msg = 'CKAN re-format error'
        self.assertDictEqual(received, expected, msg)

    def test_reformat_keys(self):
        """Re-format CKAN sanitised data structure keys.
        """
        # Given an extracted CKAN data structure
        data = {'organization|title': 'Geoscience Australia'}

        # when I reformat the organization|title field
        received = baip_loader.Loader.reformat_keys(data)

        # then the data values should be converted to a format that can
        # be ingest into CKAN
        expected = {
            'organization': {
                'title': 'Geoscience Australia'
            }
        }
        msg = 'CKAN re-format key error'
        self.assertDictEqual(received, expected, msg)

    def test_validate_string_values(self):
        """Test CKAN data validation: string values.
        """
        # Given a CKAN data structure
        ckan_data = REFORMATTED_CKAN

        # and a vocabulary set for the publisher validation_sets
        # configuration set is defined
        vocab = ['Test',
                 'geoscience australia']
        loader = baip_loader.Loader()
        loader.validation_sets = {'publisher': vocab}

        # and the rule set for the publisher mapper is defined
        levels = {'publisher': []}
        loader.ckan_mapper = levels

        # when I validate the publisher CKAN list field
        received = loader.validate(ckan_data)

        # then the CKAN data structure should be modified to conform to
        # the  publisher vocabulary
        expected = REFORMATTED_CKAN
        expected['publisher'] = 'geoscience australia'
        msg = 'Validated CKAN data error: list values'
        self.assertDictEqual(received, expected, msg)

    def test_validate_list_values(self):
        """Test CKAN data validation: list values.
        """
        # Given a CKAN data structure
        ckan_data = REFORMATTED_CKAN

        # and a vocabulary set for the geospatial_topics validation_sets
        # configuration set is defined
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
        loader = baip_loader.Loader()
        loader.validation_sets = {'geospatial_topic': vocab}

        # and the rule set for the geospatial_topic mapper is defined
        levels = {'geospatial_topic': []}
        loader.ckan_mapper = levels

        # when I validate the geospatial_topic CKAN list field
        received = loader.validate(ckan_data)

        # then the CKAN data structure should be modified to conform to
        # the  geospatial_topic vocabulary
        expected = REFORMATTED_CKAN
        expected['geospatial_topic'] = ['Environment']
        msg = 'Validated CKAN data error: list values'
        self.assertDictEqual(received, expected, msg)

    def test_validate_no_geospatial_sets_vocabulary(self):
        """Test CKAN data validation: no geospatial_sets vocabulary.
        """
        # Given a CKAN data structure
        ckan_data = REFORMATTED_CKAN

        # and a vocabulary set for the geospatial_topics validation_sets
        # configuration set is NOT defined
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
        loader = baip_loader.Loader()
        loader.validation_sets = {'geospatial_topic': vocab}

        # and the rule set for the geospatial_topic mapper is defined
        levels = {}
        loader.ckan_mapper = levels

        # when I validate the geospatial_topic CKAN field
        received = loader.validate(ckan_data)

        # then the CKAN data structure should NOT be modified
        expected = REFORMATTED_CKAN
        msg = 'Validated CKAN data error'
        self.assertDictEqual(received, expected, msg)

    def test_add_ckan_defaults(self):
        """Test add_ckan_defaults
        """
        # Given a reformatted CKAN data structure
        data = REFORMATTED_CKAN

        # and a set of ckan_defaults are added to the configuration
        owner_org = 'c5766f7d-963a-4f30-915e-f1a6f1143301'
        ckan_defaults = {'owner_org': owner_org}
        loader = baip_loader.Loader()
        loader.ckan_defaults = ckan_defaults

        # when the ckan_defaults are applied to the CKAN data structure
        received = loader.add_ckan_defaults(data)

        # then the default values should augment the CKAN data structure
        expected = DEFAULTS_CKAN
        msg = 'CKAN defaults augmented data structure error'
        self.assertDictEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._source_dir = None
        cls._results_dir = None
