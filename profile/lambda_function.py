import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    email = event['email']
    
    response = client.get_item(TableName='project-profiles', Key={'email': {'S': email}})
    
    if 'Item' in response:
        about_me = response['Item']['about_me']['S']
        group = response['Item']['group']['L']
        return {
            'statusCode': 200,
            'body': {'about_me': about_me,
                     'group': group
            }
        }
    else:
        return {
            'statusCode': 400,
            'body': "No account found"
        }

