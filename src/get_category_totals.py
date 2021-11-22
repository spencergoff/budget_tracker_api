import os

def hello_world(event, context):
    body = 'Hello, world!'
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': 'Hello, world!'
    }

# def calculate_weekly_total(dollar_amounts):
#     return ''

def add_dollar_amounts(dollar_amounts):
    total = 0
    for amount in dollar_amounts:
        total = total + amount
    formated_total = "${:,.2f}".format(total)
    return formated_total