import unittest2
import os
import tempfile

import baip_loader
from filer.files import (remove_files,
                         get_directory_files_list)


class TestIngester(unittest2.TestCase):
    """:class:`baip_loader.Ingester` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        test_file_dir = os.path.join('baip_loader',
                                     'interface',
                                     'tests',
                                     'files')
        test_json_file = 'DD006FCE-BEF5-4377-82AE-2C5A14B50E34.json'
        cls._test_json_path = os.path.join(test_file_dir, test_json_file)

    def test_init(self):
        """Initialise a baip_loader.Ingester object.
        """
        loader = baip_loader.Ingester()
        msg = 'Object is not a baip_loader.Ingester'
        self.assertIsInstance(loader, baip_loader.Ingester, msg)

    def test_source_files_empty_directory(self):
        """Source CKAN JSON files: empty directory.
        """
        # Given an empty CKAN JSON source directory
        source_dir = tempfile.mkdtemp()
        ingester = baip_loader.Ingester(source_dir=source_dir)

        # when I want to source JSON files
        received = ingester.source_files()

        # then an empty list should be returned
        expected = []
        msg = 'Source files: empty directory should return []'
        self.assertListEqual(received, expected, msg)

        # Clean up.
        os.removedirs(source_dir)

    def test_source_files_nonempty_directory(self):
        """Source CKAN JSON files: empty directory.
        """
        # Given a CKAN JSON source directory
        source_dir = tempfile.mkdtemp()
        ingester = baip_loader.Ingester(source_dir=source_dir)

        # and the directory features valid CKAN JSON files
        source_files = ['457ED79A-C6DF-4AAF-A480-00926E48CAA8.json',
                        '6151C409-0CAF-4727-9F57-00F6B71A58FB.json',
                        'banana']
        for source_file in source_files:
            source_fh = open(os.path.join(source_dir, source_file), 'w')
            source_fh.close()

        # when I want to source JSON files
        received = ingester.source_files()

        # then a list of absolute file names should be returned
        expected = [os.path.join(source_dir, i) for i in source_files]
        msg = 'Source files: non-empty directory should return matches'
        self.assertListEqual(sorted(received), sorted(expected), msg)

        # Clean up.
        remove_files(get_directory_files_list(source_dir))
        os.removedirs(source_dir)

    def test_source_files_filtered(self):
        """Source CKAN JSON files: filtered files.
        """
        # Given a CKAN JSON source directory
        source_dir = tempfile.mkdtemp()
        ingester = baip_loader.Ingester(source_dir=source_dir)

        # and the directory features valid CKAN JSON files
        source_files = ['457ED79A-C6DF-4AAF-A480-00926E48CAA8.json',
                        '6151C409-0CAF-4727-9F57-00F6B71A58FB.json']
        invalid_source_files = ['apples', 'banana']
        for source_file in (source_files + invalid_source_files):
            source_fh = open(os.path.join(source_dir, source_file), 'w')
            source_fh.close()

        # when I want to source JSON files
        received = ingester.source_files(file_filter='.*\.json')

        # then a list of absolute file names should be returned
        expected = [os.path.join(source_dir, i) for i in source_files]
        msg = 'Source files: filtered should return matches'
        self.assertListEqual(sorted(received), sorted(expected), msg)

        # Clean up.
        remove_files(get_directory_files_list(source_dir))
        os.removedirs(source_dir)

    def test_ingest(self):
        """CKAN JSON dataset ingest.
        """
        # Given a CKAN JSON file
        ckan_fh = open(self._test_json_path)
        ckan_json = ckan_fh.read()
        ckan_fh.close()

        # and a CKAN API configuration has been set
        ingester = baip_loader.Ingester()
        ingester.api_key = '524130fc-da5e-4d8c-b5c6-3e980b02f148'
        scheme = 'http'
        netloc = 'test.ddg.lws.links.com.au'
        path = '/api/action/package_create'
        ingester.csiro_uri = '{0}://{1}{2}'.format(scheme, netloc, path)

        # when I attempt a CKAN dataset ingest
        received = ingester.ingest(ckan_json, dry=True)

        # then the ingest should succeed
        msg = 'Ingest should return True'
        self.assertTrue(received, msg)

    @classmethod
    def tearDownClass(cls):
        cls._test_json_path = None
