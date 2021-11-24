import requests

def main(event, context):
    body = 'Hello, world!'
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': 'Hello, world!'
    }

# def calculate_weekly_total(dollar_amounts):
#     return ''

def get_transactions_data(url):
    transactions_response = requests.get(url)
    if transactions_response.ok == False:
        print(f'There was a {transactions_response.status_code} error getting the transactions data: {transactions_response.reason}')
        raise Exception(transactions_response.reason)
    transactions_json = transactions_response.json()
    return transactions_json

def extract_dollar_amounts_from_plaid_transactions_get(payload_plaid_transactions_get):
    amounts = []
    transactions = payload_plaid_transactions_get['transactions']
    for transaction in transactions:
        amount = transaction['amount']
        amounts.append(amount)
    return amounts

def add_dollar_amounts(dollar_amounts):
    total = 0
    for amount in dollar_amounts:
        total = total + amount
    formated_total = "${:,.2f}".format(total)
    return formated_total