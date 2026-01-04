import json
import os
import boto3
from botocore.config import Config

# Force SigV4 for S3 pre-signed URLs
s3 = boto3.client('s3', config=Config(signature_version='s4'))
BUCKET = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Debug print to see the event structure in CloudWatch
        print(f"Event: {json.dumps(event)}")
        
        # In HTTP API, the path is in 'rawPath' or 'routeKey'
        route_key = event.get('routeKey', '')
        
        # Endpoint A: POST /files
        if "POST /files" in route_key:
            body_str = event.get('body', '{}')
            # Handle cases where body might be Base64 encoded or None
            body = json.loads(body_str) if body_str else {}
            
            filename = body.get('filename', 'default-file.txt')
            
            url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={'Bucket': BUCKET, 'Key': filename},
                ExpiresIn=900 
            )
            
            return {
                "statusCode": 200,
                "body": json.dumps({"objectKey": filename, "uploadUrl": url})
            }

        # Endpoint B: GET /files/{objectKey}
        if "GET /files/" in route_key:
            params = event.get('pathParameters', {})
            object_key = params.get('objectKey')
            
            if not object_key:
                return {"statusCode": 400, "body": "Missing objectKey"}

            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': BUCKET, 'Key': object_key},
                ExpiresIn=3600
            )
            
            return {
                "statusCode": 307,
                "headers": {"Location": url}
            }

        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Route not found", "route": route_key})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }