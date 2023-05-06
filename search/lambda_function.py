import boto3
import json
import logging
import os
import time

client = boto3.client('dynamodb')

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    print("Event: {}".format(json.dumps(event)))
    
    email = event['email']
    class_value = event['class']
                
    # Find students in the same class
    classmates = {}
    
    # Define the table scan params
    scan_params = {
        'TableName': 'project-profiles',
        'FilterExpression': '#c = :class_value',
        'ExpressionAttributeValues': {
            ':class_value': {'S': class_value}
        },
        'ExpressionAttributeNames': {"#c":"class"}
    }
    
    # Scan the table
    response = client.scan(**scan_params)
    
    # Return the profiles in the same class
    classmates = response['Items']
    print("matching profiles: {}".format(classmates))
        
    print("Classmates")
    print(classmates)
    return {
        'statusCode': 200,
        'body': json.dumps(classmates)
    }
