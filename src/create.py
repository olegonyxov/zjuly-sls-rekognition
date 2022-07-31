import json
import os
import random,string
import boto3
from botocore.config import Config


BUCKET_NAME= os.environ["BUCKET_NAME"]
s3 = boto3.client(
        's3',
        region_name='us-east-1',
        # aws_access_key_id='xxx',
        # aws_secret_access_key='xxx,
        config=Config(signature_version='s3v4'),)

def handler(event, context):
    # get a new name
    blob_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    # get URL
    url= s3.generate_presigned_url('put_object', Params={'Bucket': BUCKET_NAME, 'Key': blob_id},
                                  ExpiresIn=3600, HttpMethod='PUT')
    #create blob_url
    blob_url= "s3://"+BUCKET_NAME+"/"+blob_id

    return "lalalla"

