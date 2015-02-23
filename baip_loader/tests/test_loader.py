import unittest2
import os
import tempfile

import baip_loader
from baip_loader.tests.files.iso19115_single_record import ISO19115_ITEM


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

    def test_dump_translated(self):
        """XML to JSON translated dump.
        """
        # Given a CSIRO BAIP XML metadata structure
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record.xml')

        # when an output file name is provided
        tempfile_obj = tempfile.NamedTemporaryFile()
        target_file = tempfile_obj.name
        tempfile_obj.close()

        # and I convert to JSON
        loader = baip_loader.Loader()
        loader.source(filename=source_xml_file)
        json_filename = loader.dump_translated(filename=target_file)

        # then the CSIRO BAIP JSON Metadata should be saved to file
        json_fh = open(json_filename)
        received = json_fh.read().strip()
        json_fh = None

        target_json_file = os.path.join(self._results_dir,
                                        'baip-meta-single-record.json')
        target_json_obj = open(target_json_file)
        expected = target_json_obj.read().strip()
        msg = 'Translated JSON output error'
        self.assertEqual(received, expected, msg)

        # Clean up.
        os.remove(target_file)

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
                  'description': ['%s|%s|%s|%s' %
                            ('gmd:identificationInfo',
                             'gmd:MD_DataIdentification',
                             'gmd:abstract',
                             'gco:CharacterString')]}

        # and I perform a mapping request
        loader = baip_loader.Loader()
        loader.ckan_mapper = levels
        received = loader.iso19115_to_ckan_map(xml_data)
        # Truncate the long description ...
        received['description'][0] = received['description'][0][:30] + '...'

        # then CKAN data should be extracted
        expected = {'title': [u'Victorian Aquifer Framework - Salinity'],
                    'description': [u'[This data and its metadata st...']}
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

    @classmethod
    def tearDownClass(cls):
        cls._source_dir = None
        cls._results_dir = None
