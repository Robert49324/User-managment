import aioboto3

from configs.environment import get_settings

settings = get_settings()


class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket = settings.aws_bucket

    async def __aenter__(self):
        self.client = self.session.client(
            "s3",
            endpoint_url=settings.localstack_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.s3 = await self.client.__aenter__()
        try:
            await self.s3.head_bucket(Bucket=self.bucket)
        except Exception as e:
            await self.s3.create_bucket(Bucket=self.bucket)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type, exc, tb)

    async def upload_fileobj(self, file, filename):
        try:
            await self.s3.upload_fileobj(Fileobj=file, Bucket=self.bucket, Key=filename)
            return True
        except Exception as e:
            return False
