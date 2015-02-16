import unittest2
import os

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

    @classmethod
    def tearDownClass(cls):
        cls._source_dir == None
        cls._results_dir == None
