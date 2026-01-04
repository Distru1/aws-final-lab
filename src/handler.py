import json
import os
import boto3
from botocore.config import Config

# This specific config is required for us-east-1 to avoid the "s4-query" error
s3_config = Config(
    signature_version='s3v4',
    region_name='us-east-1',
    s3={'addressing_style': 'virtual'}
)

s3 = boto3.client('s3', config=s3_config)
BUCKET = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        route_key = event.get('routeKey', '')
        
        # Endpoint A: POST /files
        if "POST /files" in route_key:
            body_str = event.get('body', '{}')
            body = json.loads(body_str) if body_str else {}
            filename = body.get('filename', 'hello.txt')
            
            # Generate the URL
            url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={'Bucket': BUCKET, 'Key': filename},
                ExpiresIn=900 
            )
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "objectKey": filename, 
                    "uploadUrl": url
                })
            }

        # Endpoint B: GET /files/{objectKey}
        if "GET /files/" in route_key:
            object_key = event['pathParameters']['objectKey']
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': BUCKET, 'Key': object_key},
                ExpiresIn=3600
            )
            return {
                "statusCode": 307,
                "headers": {"Location": url}
            }

        return {"statusCode": 404}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}