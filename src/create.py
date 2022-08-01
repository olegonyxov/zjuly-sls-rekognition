import json
import os
import random,string
import boto3
from botocore.config import Config


BUCKET_NAME= os.environ["BUCKET_NAME"]
TABLE_NAME= os.environ["TABLE_NAME"]
dynamodb_client = boto3.client("dynamodb")
s3 = boto3.client(
        's3',
        region_name='us-east-1',
        # aws_access_key_id='xxx',
        # aws_secret_access_key='xxx,
        config=Config(signature_version='s3v4'),)

def handler(event, context):
    # get body from event
    event_body = event.get("body")

    # body validation
    if not event_body:
        return {"statusCode": 400,
                "body": json.dumps({"error": "body is empty"})}

    # deserialization of request body
    request_body = json.loads(event_body)

    # callback_url validation
    callback_url = request_body.get("callback_url")
    # get a new name
    blob_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    # get URL
    url= s3.generate_presigned_url('put_object', Params={'Bucket': BUCKET_NAME, 'Key': blob_id},
                                  ExpiresIn=3600, HttpMethod='PUT')
    #create blob_url
    blob_url= "arn:aws:s3://"+BUCKET_NAME+"/"+blob_id

    # add a new item to the URL_TABLE
    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "blob_id": {"S": blob_id},
            "callback_url": {"S": callback_url}})
    asda = TABLE_NAME

    return {
        'statusCode': 200,
        'body': json.dumps({'url': url, 'callback_url': callback_url,  'blob_id': blob_id, 'asda': asda})
            }
