# pylint: disable=R0903,C0111,R0902
"""The :class:`baip_loader.LoaderDaemon` supports the daemonisation
facility for the BAIP Loader.

"""
__all__ = ["LoaderDaemon"]

import signal
import time

import daemoniser


class LoaderDaemon(daemoniser.Daemon):
    """:class:`LoaderDaemon`

    """
    dry = False
    batch = False
    conf = None
    inbound_dir = None

    def __init__(self,
                 pidfile,
                 filename=None,
                 inbound_dir=None,
                 dry=False,
                 batch=False,
                 conf=None):
        """:class:`LoaderDaemon` initialisation.

        """
        super(LoaderDaemon, self).__init__(pidfile=pidfile)

        self.filename = filename
        self._inbound_dir = inbound_dir
        self.dry = dry
        self.batch = batch
        self.conf = conf

        # If a file is provided on the command line, we want to
        # force a single iteration.
        if (self.filename is not None or self._inbound_dir is not None):
            self.batch = True

    @property
    def inbound_dir(self):
        return self._inbound_dir

    @inbound_dir.setter
    def inbound_dir(self, value):
        self._inbound_dir = value

    def _start(self, event):
        """Override the :meth:daemoniser.Daemon._start` method.

        """
        signal.signal(signal.SIGTERM, self._exit_handler)

        self.process(event)

    def process(self, event, files_to_process=None):
        """Ingest thread wrapper.  Each call to this method is
        effectively an ingest process.

        **Args:**
            *event*: a :mod:`threading.Event` based internal semaphore
            that can be set via the :mod:`signal.signal.SIGTERM` signal
            event to perform a function within the running proess.

        **Kwargs:**
            *files_to_process* override the file to process (will bypass
            a file system search)

        """
        # Check if we process the argument or the attribute filename
        # value.
        if files_to_process is None:
            if self.filename is not None:
                files_to_process = [self.filename]
            else:
                files_to_process = self.source_files(file_filter='.*\.xlm$')

        while not event.isSet():
            # Placeholder until we do real stuff.
            event.set()

            if self.dry:
                print('Dry run iteration complete')
                event.set()
            elif self.batch:
                print('Batch run iteration complete')
                event.set()
            else:
                time.sleep(self.conf.thread_sleep)

    def source_files(self, directory=None, file_filter=None):
        """Checks inbound directory (defined by the
        :attr:`geoutils.IngestConfig.inbound_dir` config option) for valid
        NITF files to be processed.

        **Returns:**
            list of matching files

        """
        pass
