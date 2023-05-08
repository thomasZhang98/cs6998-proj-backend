import json
import boto3
from boto3.dynamodb.conditions import Attr

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    email = event['email']
              
    ret = []             
    response = client.scan(
        TableName='project-group-requests',
        FilterExpression='receiver = :email',
        ExpressionAttributeValues={':email': {'S': email}}
    )
    data = response['Items']
    for i in data:
        ret.append(i['sender']['S'])
    
    return {
        'statusCode': 200,
        'body': ret
    }
