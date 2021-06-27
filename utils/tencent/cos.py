# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings


def create_bucket(bucket, region="ap-chengdu"):
    secret_id = settings.COS_ID      # 替换为用户的 secretId(登录访问管理控制台获取)
    secret_key = settings.COS_KEY      # 替换为用户的 secretKey(登录访问管理控制台获取)

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=bucket,
        ACL="public-read"
    )


def upload_files(bucket, region, file_object, key):
    secret_id = settings.COS_ID      # 替换为用户的 secretId(登录访问管理控制台获取)
    secret_key = settings.COS_KEY      # 替换为用户的 secretKey(登录访问管理控制台获取)

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    # 2. 获取客户端对象
    client = CosS3Client(config)

    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key=key,
    )

    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket.lower(), region, key)