import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    sender = event['sender']
    recipient = event['receive']
    answer = event['answer']
    request_id = event['request_id']
    
    
    #add each email to group attribute of profiles db
    if answer=="yes":
        #update sender's profile
        new_group = recipient
        response = client.update_item(
            TableName='project-profiles',
            Key={'email': {'S': sender}},
            UpdateExpression='ADD #group :new_group',
            ExpressionAttributeNames={'#group': 'group'},
            ExpressionAttributeValues={':new_group': {'S': [new_group]}}
        )
        
        #update recipient's profile
        new_group = sender
        response = client.update_item(
            TableName='project-profiles',
            Key={'email': {'S': recipient}},
            UpdateExpression='SET #group :new_group',
            ExpressionAttributeNames={'#group': 'group'},
            ExpressionAttributeValues={':new_group': {'S': [new_group]}}
        )
            
    #delete the request from the group invites db (project-group-requests)
    response = client.delete_item(
            TableName='project-group-requests',
            Key={'request_id': {'S': request_id}}
        )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

