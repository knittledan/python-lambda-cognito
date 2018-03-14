import logging
import boto3
from botocore.client import ClientError
from io import BytesIO
from botocore.exceptions import ParamValidationError


class S3:
    def __init__(self, bucket_name):
        self.log = logging.getLogger()
        self.bucket_name = bucket_name
        self.resource    = None
        self.bucket      = None

        self.set_resource()
        self.create_bucket()

    def __repr__(self):
        return self.bucket_name

    def set_resource(self):
        if boto3.DEFAULT_SESSION:
            self.resource = boto3.DEFAULT_SESSION.resource('s3')

    def create_bucket(self):
        try:
            self.resource.meta.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.resource.create_bucket(
                ACL='private',
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.resource.meta.client.meta.region_name
                }
            )
        self.bucket = self.resource.Bucket(self.bucket_name)

    def check_bucket_exists(self) -> bool:
        if self.resource:
            try:
                if self.resource.meta.client.head_bucket(Bucket=self.bucket_name):
                    return True
            except Exception as e:
                self.log.error(f"S3 bucket {self.bucket_name} doesnt exist. {e}")
        return False

    def delete_bucket(self):
        for key in self.bucket.objects.all():
            key.delete()
        self.bucket.delete()

    def upload(self, payload, file_name):
        try:
            return self.bucket.put_object(Body=payload, Key=file_name, ContentType=extract_content_type(file_name))
        except ClientError as e:
            msg = f"{str(e)} {file_name}"
            self.log.exception(msg)

    def delete(self, file_name):
        try:
            return self.bucket.delete_objects(Delete={
                'Objects': [
                    {'Key': file_name}
                ]
            })
        except (ClientError, ParamValidationError) as e:
            msg = f"{str(e)} {self.bucket_name} - {file_name}"
            self.log.exception(msg)

    def download(self, file_name) -> bytes:
        try:
            with BytesIO() as f:
                self.bucket.download_fileobj(file_name, f)
                f.seek(0)
                return f.read()
        except (ClientError, ParamValidationError) as e:
            msg = f"{str(e)} {self.bucket_name} - {file_name}"
            self.log.exception(msg)

    def exists(self, file_name) -> bool:
        try:
            _ = self.resource.Object(self.bucket_name, file_name).last_modified
            return True
        except (ClientError, ParamValidationError) as e:
            self.log.debug(f"File doesnt exist in {self.bucket_name} {file_name}")
        return False
