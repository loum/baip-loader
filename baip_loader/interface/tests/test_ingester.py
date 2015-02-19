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
        cls._source_dir = os.path.join('baip_loader', 'tests', 'files')

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
        for file in source_files:
            source_fh = open(os.path.join(source_dir, file), 'w')
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
        for file in (source_files + invalid_source_files):
            source_fh = open(os.path.join(source_dir, file), 'w')
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

    @classmethod
    def tearDownClass(cls):
        cls._source_dir = None
