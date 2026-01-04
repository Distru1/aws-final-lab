import json
import os
import boto3
from botocore.config import Config

s3 = boto3.client('s3', config=Config(signature_version='s4'))
BUCKET = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    route_key = event['routeKey']
    
    # Endpoint A: POST /files (Upload Preparation)
    if route_key == "POST /files":
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename', 'upload.dat')
        
        # Generate PUT presigned URL (valid for 15 mins)
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': BUCKET, 'Key': filename},
            ExpiresIn=900 
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"objectKey": filename, "uploadUrl": url})
        }

    # Endpoint B: GET /files/{objectKey} (Download Redirect)
    if "GET /files/" in route_key:
        object_key = event['pathParameters']['objectKey']
        
        # Generate GET presigned URL (valid for 1 hour)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET, 'Key': object_key},
            ExpiresIn=3600
        )
        
        # 307 Temporary Redirect is chosen to preserve the request semantics
        return {
            "statusCode": 307,
            "headers": {"Location": url}
        }

    return {"statusCode": 404}