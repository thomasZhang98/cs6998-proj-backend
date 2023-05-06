import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)
    # TODO implement
    email = event['email']
    response = client.get_item(TableName='project-professors', Key={'email': {'S': email}})
    if 'Item' not in response:
        response = client.put_item(TableName='project-professors', Item={'email': {'S': email}})
    print(response)
    return {
        'statusCode': 200,
        'body': response
    }