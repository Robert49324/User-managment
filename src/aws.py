import asyncio

import aioboto3

from config import settings


class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket = settings.aws_bucket
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_bucket())

    async def create_bucket(self):
        async with self.session.client(
            "s3",
            endpoint_url=settings.localstack_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        ) as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket)
            except s3.exceptions.ClientError as e:
                await s3.create_bucket(Bucket=self.bucket)

    async def upload_fileobj(self, file, filename):
        async with self.session.client(
            "s3",
            endpoint_url=settings.localstack_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        ) as s3:
            try:
                await s3.upload_fileobj(file, self.bucket, filename)
                return True
            except Exception as e:
                return False


def get_s3_client():
    return S3Client()
