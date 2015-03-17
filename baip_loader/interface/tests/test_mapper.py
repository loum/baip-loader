import unittest2
import os
import tempfile

import baip_loader
from filer.files import (copy_file,
                         remove_files,
                         get_directory_files_list)
from baip_loader.interface.tests.files.ckan_mapped_dict import CKAN_MAPPED


class TestMapper(unittest2.TestCase):
    """:class:`baip_loader.Mapper` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls._source_dir = os.path.join('baip_loader', 'tests', 'files')
        cls._results_dir = os.path.join('baip_loader', 'tests', 'results')
        cls._test_target_dir = tempfile.mkdtemp()

    def test_init(self):
        """Initialise a baip_loader.Mapper object.
        """
        xlator = baip_loader.Mapper()
        msg = 'Object is not a baip_loader.Mapper'
        self.assertIsInstance(xlator, baip_loader.Mapper, msg)

    def test_mapper(self):
        """Mapper interface.
        """
        # Given a CSIRO BAIP ISO19115 XML file
        source_xml_file = 'baip-meta-single-record.xml'
        test_file = os.path.join(self._test_target_dir, source_xml_file)
        copy_file(os.path.join(self._source_dir, source_xml_file),
                  test_file)

        # and a CKAN mapper configuration is defined
        conf_file = os.path.join('baip_loader', 'conf', 'loader.conf')
        conf = baip_loader.LoaderConfig(conf_file)
        conf.parse_config()

        # and basic defaults defined
        defaults = {'default': 'test default value'}

        mapper = baip_loader.Mapper()
        mapper.loader.ckan_mapper = conf.ckan_mapper
        mapper.loader.ckan_defaults = defaults

        # and a target directory is defined
        mapper.target_dir = self._test_target_dir

        # when I extract the XML and convert to a CKAN data-ingestable
        # structure
        received = mapper.xml_to_ckan_map(infile=test_file)

        # then the CSIRO BAIP Metadata should be saved to file as JSON
        expected = [os.path.join(self._test_target_dir,
                                 'DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json')]
        msg = 'List of XML to CKAN files written error'
        self.assertListEqual(received, expected, msg)

        # Clean up.
        remove_files(get_directory_files_list(self._test_target_dir))

    def test_dump_ckan_data(self):
        """Dump CKAN data structure.
        """
        # Given a CKAN data structure
        guid = CKAN_MAPPED.keys()[0]
        data = CKAN_MAPPED.get(guid)

        # and a target base directory
        mapper = baip_loader.Mapper(target_dir=self._test_target_dir)

        # when I write out the CKAN data structure
        received = mapper.dump_ckan_data(guid, data)

        # the JSON files should be written to the filesystem
        expected = os.path.join(self._test_target_dir,
                                'DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json')
        msg = 'Written CKAN JSON files error'
        self.assertEqual(received, expected, msg)

        # Clean up.
        remove_files(expected)

    @classmethod
    def tearDownClass(cls):
        cls._source_dir = None
        cls._results_dir = None

        os.removedirs(cls._test_target_dir)
        cls._test_target_dir = None
