import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)
    # TODO implement
    name = event['name']
    email = event['professor_email']
    size = event['max_group_size']
    
    
    response = client.get_item(TableName='project-class', Key={'name': {'S': name}})
    if 'Item' not in response:
        response = client.put_item(TableName='project-class', Item={
            'name': {'S': name}, 
            'prof_email': {'S': email},
            'max_group_size': {'S': size},
            }
        )
        return {
        'statusCode': 200,
        'body': response
        }
    print(response)
    return {
        'statusCode': 200,
        'body': 'invalid'
    }