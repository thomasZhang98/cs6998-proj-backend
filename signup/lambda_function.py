import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)
    email = event['email']
    class_name = event['class']
    response = client.get_item(TableName='project-class', Key={'name': {'S': class_name}})
    print(response)
    size = int(response['Item']['max_group_size']['S'])
    group = [{'S': ""}] * (size-1)
    print(group)
    
    response = client.put_item(TableName='project-profiles', Item={
            'email': {'S': email}, 
            'class': {'S': class_name},
            'group': {'L': group},
            'about_me': {'S': ''}
        }
    )
    
    print(response)
    # TODO implement
    return {
        'statusCode': 200,
        'body': response
    }
