import os

def hello_world(event, context):
    body = 'Hello, world!'
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': 'Hello, world!'
    }

def get_expected_weekly_total():
    return ''