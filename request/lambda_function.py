import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    email = event['email']
    clas = event['class']
    link = 'http://coms6998p4.s3-website-us-east-1.amazonaws.com'
    
    messageToSend = """
    You have been invited to find project teammates for your group project in
    {}. Follow this link to start finding teammates!\n{}
    """.format(clas, link)
    
    
    #sender must be verified with SES
    SENDER = "ar4513@columbia.edu"
    RECIPIENT = email
    AWS_REGION = "us-east-1"
    SUBJECT = "You've Been Invited to Find Project Teammates!"
    BODY_TEXT = messageToSend
    BODY_HTML = """<html>
    <head></head>
    <body>
      <p> {messageToSend} </p>
    </body>
    </html>""".format(messageToSend=messageToSend)            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
    }