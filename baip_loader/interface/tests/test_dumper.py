import unittest2
import os
import tempfile

import baip_loader
from filer.files import (remove_files,
                         get_directory_files_list)


class TestDumper(unittest2.TestCase):
    """:class:`baip_loader.Dumper` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls._source_dir = os.path.join('baip_loader', 'tests', 'files')
        cls._results_dir = os.path.join('baip_loader', 'tests', 'results')

    def test_init(self):
        """Initialise a baip_loader.Dumper object.
        """
        dumper = baip_loader.Dumper()
        msg = 'Object is not a baip_loader.Dumper'
        self.assertIsInstance(dumper, baip_loader.Dumper, msg)

    def test_dump(self):
        """Dump interface.
        """
        # Given I launch the baip-loader tool from the command line with the
        # dump sub-command
        dumper = baip_loader.Dumper()

        # and the -i or --input-file switch is provided with a CSIRO BAIP
        # XML file name supplied as an argument
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-multiple-records.xml')

        # then the CSIRO BAIP Metadata should be saved to as individual
        # JSON files
        dumper.target_dir = tempfile.mkdtemp()
        received = dumper.dump(uri=None, infile=source_xml_file)
        json_files = ['457ED79A-C6DF-4AAF-A480-00926E48CAA8.json',
                      '6151C409-0CAF-4727-9F57-00F6B71A58FB.json',
                      '6968B11F-9912-42CA-8536-00CDE75E75D9.json',
                      '781A8B81-93B8-4CDE-9B56-00291D7543EA.json']
        expected = [os.path.join(dumper.target_dir, i) for i in json_files]
        msg = 'JSON files created error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

        # Clean up.
        remove_files(get_directory_files_list(dumper.target_dir))
        os.removedirs(dumper.target_dir)

    @classmethod
    def tearDownClass(cls):
        cls._source_dir = None
        cls._results_dir = None
