import json
import boto3
import requests
import datetime
import calendar

def main(event, context):
    print(f'Made it to main')
    start_date = get_last_thursday_date()
    end_date = str(datetime.date.today())
    total = calculate_weekly_total(start_date, end_date)
    print(f'total: {total}')
    api_gateway_response = {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': f'Total spent since Thursday: {total}'
    }
    print(f'api_gateway_response: {api_gateway_response}')
    return api_gateway_response

def get_last_thursday_date():
    today = datetime.date.today()
    offset = (today.weekday() - calendar.THURSDAY) % 7
    last_thursday_date = str(today - datetime.timedelta(days=offset))
    print(f'last_thursday_date: {last_thursday_date}')
    return last_thursday_date

def calculate_weekly_total(start_date, end_date):
    print(f'Made it to calculate_weekly_total')
    url_plaid_transactions_get = 'https://development.plaid.com/transactions/get'
    transactions_data = get_transactions_data(url_plaid_transactions_get, start_date, end_date)
    transaction_amounts = extract_dollar_amounts_from_plaid_transactions_get(transactions_data)
    total = add_dollar_amounts(transaction_amounts)
    return total

def get_transactions_data(url_plaid_transactions_get, start_date, end_date):
    print(f'Made it to get_transactions_data')
    plaid_dev_secret = get_secret('plaid_dev_secret')
    plaid_dev_access_token = get_secret('plaid_dev_access_token')
    data = {
            'client_id': '5f49268da466f10010ef7ce2',
            'secret': plaid_dev_secret,
            'access_token': plaid_dev_access_token,
            'start_date': start_date,
            'end_date': end_date
            }
    headers = {'Content-Type': 'application/json'}
    transactions_response = requests.post(url_plaid_transactions_get, data=json.dumps(data), headers=headers)
    if transactions_response.ok == False:
        explanation = f'There was a {transactions_response.status_code} error getting the transactions data: {transactions_response.reason}. \n\n headers: {headers}'
        print(explanation)
        raise Exception(explanation)
    transactions_json = transactions_response.json()
    print(f'transactions_json: {transactions_json}')
    return transactions_json

def extract_dollar_amounts_from_plaid_transactions_get(payload_plaid_transactions_get):
    print(f'Made it to extract_dollar_amounts_from_plaid_transactions_get')
    print(f'payload_plaid_transactions_get: {payload_plaid_transactions_get}')
    my_credit_card_account_id = 'eO50JxE95whkXAVjg7nZu4zJ4ynKjMCdbXen0'
    amounts = []
    transactions = payload_plaid_transactions_get['transactions']
    for transaction in transactions:
        if transaction['account_id'] == my_credit_card_account_id:
            amount = transaction['amount']
            amounts.append(amount)
    print(f'amounts: {amounts}')
    return amounts

def add_dollar_amounts(dollar_amounts):
    print(f'Made it to add_dollar_amounts')
    total = 0
    for amount in dollar_amounts:
        total = total - amount
    formated_total = '${:,.2f}'.format(total)
    print(f'formated_total: {formated_total}')
    return formated_total

def get_secret(secret_name):
    print(f'Made it to get_secret with secret_name: {secret_name}')
    region_name = 'us-east-1'
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    secret_payload = client.get_secret_value(SecretId=secret_name)
    secret_value = extract_secret_from_payload(secret_name, secret_payload)
    return secret_value

def extract_secret_from_payload(secret_name, secret_payload):
    try:
        all_secrets = json.loads(secret_payload['SecretString'])
    except:
        secret_value = secret_payload['SecretString']
    else:
        secret_value = all_secrets[secret_name]
    return secret_value
    