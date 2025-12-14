import boto3
from uuid import uuid4
import time

dynamodb = boto3.resource('dynamodb')
dynamoTable = dynamodb.Table('bronzeMetadata')

secondsConvert30Days = 30 * 24 * 60 * 60
ttl_timestamp = int(time.time()) + secondsConvert30Days

def lambda_handler(event, context):
    records = event.get('Records', [])

    for record in records:
        s3_info = record.get('s3', {})
        bucket_name = s3_info.get('bucket', {}).get('name')
        object_key = s3_info.get('object', {}).get('key')
        size = s3_info.get('object', {}).get('size', -1)
        event_name = record.get('eventName', 'Object Created')
        event_time = record.get("eventTime")

        if bucket_name and object_key:
            dynamoTable.put_item(Item={
                'Resource_id': str(uuid4()),
                'Bucket': bucket_name,
                'Object': object_key,
                'Size': size,
                'Event': event_name,
                'EventTime': event_time,
                'TimeToExist': ttl_timestamp
            })