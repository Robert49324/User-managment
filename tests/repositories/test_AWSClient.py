import pytest
from unittest.mock import MagicMock, AsyncMock

from repositories.AWSClient import S3Client

@pytest.fixture
def s3_client():
    return S3Client()

@pytest.mark.asyncio
async def test_upload_fileobj_success(s3_client):
    s3_client.session.client = AsyncMock()
    s3_client.session.client.return_value.__aenter__.return_value.upload_fileobj = AsyncMock(return_value=True)
    s3_client.session.client.return_value.__aenter__.return_value.head_bucket = AsyncMock()
    
    file = MagicMock()
    filename = "test_file.txt"
    result = await s3_client.upload_fileobj(file, filename)
    print("Result:", result)
    assert result is True
@pytest.mark.asyncio
async def test_upload_fileobj_failure(s3_client):
    s3_client.session.client = AsyncMock()
    s3_client.session.client.return_value.__aenter__.return_value.upload_fileobj = AsyncMock(side_effect=Exception())
    
    file = MagicMock()
    filename = "test_file.txt"
    result = await s3_client.upload_fileobj(file, filename)
    assert result is False
