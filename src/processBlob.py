import json
import os
import urllib
import boto3
from botocore.config import Config


BUCKET_NAME= os.environ["BUCKET_NAME"]
s3 = boto3.client(
        's3',
        region_name='us-east-1',
        # aws_access_key_id='xxx',
        # aws_secret_access_key='xxx,
        config=Config(signature_version='s3v4'),)
def process(event,context):
    bucket=event['Records'][0]['s3']['bucket']['name']
    key= urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key = key)
        text= response["Body"].read().decode()
        data = json.loads(text)
        print(data)
        return "Success"
    except Exception as e:
        print(e)
        raise e

