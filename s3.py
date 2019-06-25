
import boto
from boto.s3.key import Key


class S3BucketAdapter(object):

    def __init__(self, bucket_name, S3_settings):
        if bucket_name is None:
            raise Exception('No S3 bucket specified')
        self._bucket_name = bucket_name
        self._S3_settings = S3_settings
        self._bucket = None
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self._conn = boto.connect_s3(
                aws_access_key_id=self._S3_settings.ACCESS_KEY_ID,
                aws_secret_access_key=self._S3_settings.SECRET_ACCESS_KEY,
                host=self._S3_settings.S3_HOST
            )
        return self._conn
    
    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = self.conn.get_bucket(self._bucket_name)
        return self._bucket

    def upload_file(self, content, key_value, content_type=None, public=False, cached=False):
        key = Key(self.bucket)
        key.key = key_value

        if content_type is not None:
            key.set_metadata('Content-Type', content_type)

        if cached:
            key.set_metadata('Cache-Control', 'max-age=31536000, public')
            key.set_metadata('Expires', 'Sun, 01 Jan 2034 00:00:00 GMT')

        key.set_contents_from_file(content)
        content.seek(0)

        if public:
            key.make_public()

    def download_file(self, key_value, output_file):
        key = Key(self.bucket)
        key.key = key_value
        key.get_contents_to_file(output_file)
