import json
import boto3
from datetime import datetime

client = boto3.client('dynamodb')

def compute_recommendation(day1, day2):
    common_slots = []
    i = 0
    j = 0
    while i < len(day1) and j < len(day2):
        day1_start, day1_end = day1[i].split('-')
        day2_start, day2_end = day2[j].split('-')
        day1_start = datetime.strptime(day1_start, "%H:%M:%S")
        day1_end = datetime.strptime(day1_end, "%H:%M:%S")
        day2_start = datetime.strptime(day2_start, "%H:%M:%S")
        day2_end = datetime.strptime(day2_end, "%H:%M:%S")
        if day1_end <= day2_start:
            i += 1
        elif day1_start >= day2_end:
            j += 1
        else:
            start_time = max(day1_start, day2_start)
            if day1_end < day2_end:
                common_slots.append((start_time, day1_end))
                i += 1
            else:
                common_slots.append((start_time, day2_end))
                j += 1
    return common_slots

def generate_recommendation(event, item):
    other_email = item['email']['S']
    recommendation = {}
    for key, values in item.items():
        if key != 'email' and event[key]['L'] and values['L']:
            common_slots = compute_recommendation(revert_dict(event[key]['L']), revert_dict(values['L']))
            if common_slots:
                recommendation[key] = common_slots
    
    if recommendation:
        return recommendation
    else:
        return {}

def convert_dict(input_list):
    output = []
    for item in input_list:
        output.append({'S': item})
    return output
    
def revert_dict(input_list):
    output = []
    for item in input_list:
        output.append(item['S'])
    return output

def lambda_handler(event, context):
    print(event)
    email = event['email']
    
    # Find own availability
    response = client.get_item(TableName='project-availabilities', Key={'email': {'S': email}})
    self_avails = response['Item']
    
    # Find common slots among students
    recommendations = {}
    response = client.scan(TableName='project-availabilities')
    data = response['Items']
    
    for item in data:
        if item['email']['S'] != email:
            recommendations[item['email']['S']] = generate_recommendation(self_avails, item)
    
    results = []
    for user, days in recommendations.items():
        total_seconds = 0
        for day, times in days.items():
            for time in times:
                total_seconds += (time[1] - time[0]).seconds
        results.append((total_seconds, user))
    results.sort(reverse=True)
    
    print(results)
    results = list(map(lambda x: x[1], results))

    # TODO implement
    return {
        'statusCode': 200,
        'body': results[:10]
    }
