import unittest2
import os
import tempfile

import baip_loader


class TestTranslator(unittest2.TestCase):
    """:class:`baip_loader.Translator` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls._source_dir = os.path.join('baip_loader', 'tests', 'files')
        cls._results_dir = os.path.join('baip_loader', 'tests', 'results')

    def test_init(self):
        """Initialise a baip_loader.Translator object.
        """
        xlator = baip_loader.Translator()
        msg = 'Object is not a baip_loader.Translator'
        self.assertIsInstance(xlator, baip_loader.Translator, msg)

    def test_translate(self):
        """Translate interface.
        """
        # Given I launch the baip-loader tool from the command line with the
        # translate sub command
        xlator = baip_loader.Translator()

        # and the -i or --input-file switch is provided with a CSIRO BAIP
        # XML file name supplied as an argument
        source_xml_file = os.path.join(self._source_dir,
                                       'baip-meta-single-record.xml')

        # and the -o or --output-file switch is provided with an output
        # file suppliled as an argument
        tempfile_obj = tempfile.NamedTemporaryFile()
        target_file = tempfile_obj.name
        tempfile_obj.close()

        # then the CSIRO BAIP Metadata should be saved to file as JSON
        json_filename = baip_loader.Translator.translate(uri=None,
                                                         infile=source_xml_file,
                                                         outfile=target_file)

        json_filename_fh = open(json_filename)
        received = json_filename_fh.read()
        json_filename_fh.close()

        target_json_file = os.path.join(self._results_dir,
                                        'baip-meta-single-record.json')
        target_json_obj = open(target_json_file)
        expected = target_json_obj.read().strip()
        msg = 'Translated JSON output error'
        self.assertEqual(received, expected, msg)

        # Clean up.
        os.remove(json_filename)

    @classmethod
    def tearDownClass(cls):
        cls._source_dir == None
        cls._results_dir == None
