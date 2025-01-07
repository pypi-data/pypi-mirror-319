import os
import boto3
from botocore.client import Config

def get_s3_client(endpoint_url=None, aws_access_key_id=None, 
                  aws_secret_access_key=None, region=None):
    """创建 S3 客户端连接
    
    所有参数都可以从环境变量获取:
    - S3_ENDPOINT_URL: S3 端点 URL
    - AWS_ACCESS_KEY_ID: AWS 访问密钥 ID
    - AWS_SECRET_ACCESS_KEY: AWS 密钥
    - AWS_REGION: AWS 区域
    """
    endpoint_url = endpoint_url or os.getenv('S3_ENDPOINT_URL')
    aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    region = region or os.getenv('AWS_REGION', 'us-east-1')

    # 配置 S3 客户端
    s3_config = Config(
        connect_timeout=5,
        retries={'max_attempts': 3},
        signature_version='s3v4'
    )

    return boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
        config=s3_config
    )

def get_s3_resource(endpoint_url=None, aws_access_key_id=None, 
                    aws_secret_access_key=None, region=None):
    """创建 S3 资源对象"""
    endpoint_url = endpoint_url or os.getenv('S3_ENDPOINT_URL')
    aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    region = region or os.getenv('AWS_REGION', 'us-east-1')

    return boto3.resource(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    ) 