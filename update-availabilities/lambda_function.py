import json
import boto3
from datetime import datetime
from collections import defaultdict

client = boto3.client('dynamodb')

day_convert_map = {
    'Monday': 'mon',
    'Tuesday': 'tue',
    'Wednesday': 'wed',
    'Thursday': 'thu',
    'Friday': 'fri',
    'Saturday': 'sat',
    'Sunday': 'sun'
}

def convert_dict(input_list):
    output = []
    for item in input_list:
        output.append({'S': item})
    return output
    
def lambda_handler(event, context):
    email = event['email']
    events = event['events']
    start_of_day = "06:00:00"
    end_of_day = "22:00:00"
    
    result = defaultdict(list)
    for event in events:
        date = event['start'].split('T')[0]
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        day_str = date_obj.strftime('%A')
        
        start_time = event['start'].split('T')[1].split('-')[0]
        end_time = event['end'].split('T')[1].split('-')[0]
        
        result[day_convert_map[day_str]].append((start_time, end_time))

    print(result)
    
    for day, events in result.items():
        if events:
            free_slots = []
            curr_start_time = start_of_day
            for i in range(len(events)):
                free_slots.append('-'.join([curr_start_time, events[i][0]]))
                curr_start_time = events[i][1]
            free_slots.append('-'.join([curr_start_time, end_of_day]))
            result[day] = free_slots
        else:
            result[day] = ['-'.join([start_of_day, end_of_day])]
    
    print(result)
    
    response = client.put_item(TableName='project-availabilities', Item={
        'email': {'S': email},
        'mon': {'L': convert_dict(result['mon'])},
        'tue': {'L': convert_dict(result['tue'])},
        'wed': {'L': convert_dict(result['wed'])},
        'thu': {'L': convert_dict(result['thu'])},
        'fri': {'L': convert_dict(result['fri'])},
        'sat': {'L': convert_dict(result['sat'])},
        'sun': {'L': convert_dict(result['sun'])}
    })
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': response
    }
