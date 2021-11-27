import json
import boto3
import requests

def main(event, context):
    total = calculate_weekly_total()
    return total

def calculate_weekly_total():
    url_plaid_transactions_get = 'https://development.plaid.com/transactions/get'
    transactions_data = get_transactions_data(url_plaid_transactions_get)
    transaction_amounts = extract_dollar_amounts_from_plaid_transactions_get(transactions_data)
    total = add_dollar_amounts(transaction_amounts)
    return total

def get_transactions_data(url_plaid_transactions_get):
    plaid_dev_secret = get_secret('plaid_dev_secret')
    plaid_dev_access_token = get_secret('plaid_dev_access_token')
    data = {
            "client_id": "5f49268da466f10010ef7ce2",
            "secret": plaid_dev_secret,
            "access_token": plaid_dev_access_token,
            "start_date": "2021-11-20",
            "end_date": "2021-11-27"
            }
    headers = {"Content-Type": "application/json"}
    transactions_response = requests.post(url_plaid_transactions_get, data=data, headers=headers)
    if transactions_response.ok == False:
        explanation = f'There was a {transactions_response.status_code} error getting the transactions data: {transactions_response.reason}. \n\n data: {data} \n\n headers: {headers}'
        print(explanation)
        raise Exception(explanation)
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

def get_secret(secret_name):
    region_name = 'us-east-1'
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']['secret_name']
    return secret