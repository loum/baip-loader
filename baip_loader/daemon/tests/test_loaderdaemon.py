# pylint: disable=R0904,C0103
""":class:`baip_loader.LoaderDaemon` tests.

"""
import unittest2

import baip_loader


class TestLoaderDaemon(unittest2.TestCase):
    """:class:`baip_loader.LoaderDaemon` test cases.
    """
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

        cls._conf = baip_loader.LoaderConfig()

    def setUp(self):
        self._loaderd = baip_loader.LoaderDaemon(pidfile=None,
                                                 conf=self._conf)

    def test_init(self):
        """Initialise a LoaderDaemon object.
        """
        msg = 'Object is not a baip_loader.LoaderDaemon'
        self.assertIsInstance(self._loaderd, baip_loader.LoaderDaemon, msg)

    def tearDown(self):
        del self._loaderd

    @classmethod
    def tearDownClass(cls):
        del cls._conf
