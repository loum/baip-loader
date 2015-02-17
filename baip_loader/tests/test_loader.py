import unittest2
import os
import tempfile

import baip_loader


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
        expected = [u'781A8B81-93B8-4CDE-9B56-00291D7543EA',
                    u'457ED79A-C6DF-4AAF-A480-00926E48CAA8',
                    u'6968B11F-9912-42CA-8536-00CDE75E75D9',
                    u'6151C409-0CAF-4727-9F57-00F6B71A58FB']
        msg = 'list of GUIDs incorrect'
        self.assertListEqual(received, expected, msg)

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
        expected = [u'DD006FCE-BEF5-4377-82AE-2C5A14B50E34']
        msg = 'list of GUIDs incorrect'
        self.assertListEqual(received, expected, msg)

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

        loader = baip_loader.Loader()
        received = loader.extract_guid(source_dict['gmd:MD_Metadata'])
        expected = 'DD006FCE-BEF5-4377-82AE-2C5A14B50E34'
        msg = 'Extracted GUID error'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        cls._source_dir == None
        cls._results_dir == None
