import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    sender = event['sender']
    recipient = event['receive']
    answer = event['answer']
    #request_id = event['request_id']
    
    
    #add each email to group attribute of profiles db
    if answer=="yes":
        #update sender's profile
        response = client.get_item(TableName='project-profiles', Key={'email': {'S': sender}})
        curr_group = response['Item']['group']['L']
        print("curr group: {}".format(curr_group))
        for i in curr_group:
            if i['S']=='':
                i['S']=recipient
                break
        new_group=curr_group
        print("new group: {}".format(new_group))
        item={
            'email':{'S':sender},
            'class':response['Item']['class'],
            'group':{'L':new_group}
        }
        response = client.put_item(TableName='project-profiles', Item=item)
        
        #update recipient's profile
        response = client.get_item(TableName='project-profiles', Key={'email': {'S': recipient}})
        curr_group = response['Item']['group']['L']
        print("curr group: {}".format(curr_group))
        for i in curr_group:
            if i['S']=='':
                i['S']=sender
                break
        new_group=curr_group
        print("new group: {}".format(new_group))
        item={
            'email':{'S':recipient},
            'class':response['Item']['class'],
            'group':{'L':new_group}
        }
        response = client.put_item(TableName='project-profiles', Item=item)
            
    #delete the request from the group invites db (project-group-requests)
    #get request_id
    response = client.scan(TableName='project-group-requests')
    data = response['Items']
    for d in data:
        if d['sender']['S']==sender and d['receiver']['S']==recipient:
            request_id=d['request_id']['S']
    
    response = client.delete_item(
            TableName='project-group-requests',
            Key={'request_id': {'S': request_id}}
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
