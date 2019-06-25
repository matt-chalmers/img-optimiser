
from tempfile import TemporaryFile
from retry import retry
import tinify

from s3 import S3BucketAdapter


_INITIALISED = False


def init(tiny_key):
    global _INITIALISED
    tinify.key = tiny_key
    _INITIALISED = True


_RETRY = retry(
    exceptions=(tinify.ServerError, tinify.ConnectionError),
    tries=10,
    delay=5,
    max_delay=5,
    backoff=1
)


class TinyImageOptimiser:

    def __init__(self):
        if not _INITIALISED:
            raise Exception('Module not initialised')

        self._tiny_ref = None

    def _require_loaded(self):
        if not self._tiny_ref:
            raise Exception('Image not loaded')

    # Methods to load a file into the optimiser

    @_RETRY
    def load_file(self, filename_or_obj):
        self._tiny_ref = tinify.from_file(filename_or_obj)

    @_RETRY
    def load_buffer(self, buffer):
        self._tiny_ref = tinify.from_buffer(buffer.read())

    @_RETRY
    def load_url(self, url):
        self._tiny_ref = tinify.from_url(url)

    def load_s3(self, bucket_name, key):
        tmp = TemporaryFile()
        S3BucketAdapter(bucket_name).download_file(key, tmp)
        tmp.seek(0)
        self.load_file(tmp)

    # Methods to write the optimised file to a destination

    @_RETRY
    def to_file(self, filename_or_obj):
        self._require_loaded()
        self._tiny_ref.to_file(filename_or_obj)

    @_RETRY
    def to_buffer(self):
        self._require_loaded()
        self._tiny_ref.to_buffer()

    def to_s3(self, bucket_name, key, public, cached):
        self._require_loaded()
        tmp = TemporaryFile()
        self.to_file(tmp)
        tmp.seek(0)
        S3BucketAdapter(bucket_name).upload_file(tmp, key, content_type='image', public=public, cached=cached)

