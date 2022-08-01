import os
import json
import boto3


dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]

def handler(event, context):
    # get url_id from event
    blob_id = event["pathParameters"]["blob_id"]

    # get an item from URL_TABLE
    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"blob_id": {"S": blob_id}}).get("Item")

    # result validation
    if not result:
        return {"statusCode": 404,
                "body":json.dumps({"error": "URL not found"})}

    #get long_utl from result
    callback_url= result.get("callback_url").get("S")

    #make redirect to long_url
    response = {
        'statusCode': 200,
        'body': json.dumps({'callback_url': callback_url, 'blob_id': blob_id})
            }
    return response