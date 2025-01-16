import json
import boto3
import base64

# AWS Lambda Function to Add Two Numbers
def lambda_handler_add(event, context):
    num1 = event.get('num1', 0)
    num2 = event.get('num2', 0)
    result = num1 + num2

    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }

# AWS Lambda Function to Store a File in S3
def lambda_handler_store(event, context):
    s3 = boto3.client('s3')
    bucket_name = event.get('store_doc')
    file_name = event.get('doc_file')
    file_content = base64.b64decode(event.get('file_content', ''))
    if not bucket_name or not file_name or not file_content:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing required parameters'})
        }

    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File uploaded successfully!'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'File upload failed.', 'error': str(e)})
        }
