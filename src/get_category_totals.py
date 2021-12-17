import json
import boto3
import requests
import datetime
import calendar

def main(event, context):
    print(f'Made it to main')
    url_plaid_transactions_get = 'https://development.plaid.com/transactions/get'
    start_date = get_last_thursday_date()
    end_date = get_todays_date()
    transactions_data = get_transactions_data(url_plaid_transactions_get, start_date, end_date)
    category_amounts = get_category_totals(transactions_data)
    total = add_dollar_amounts(category_amounts.values())
    body = f'\
        Amounts spent since last Thursday\
        total: {total} / $400\
        fun: {category_amounts["fun"]} / $150\
        predictable_necessities: {category_amounts["predictable_necessities"]} / $100\
        unpredictable_necessities: {category_amounts["unpredictable_necessities"]} / $50\
        other: {category_amounts["other"]} / $100'
    api_gateway_response = {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': body
    }
    print(f'api_gateway_response: {api_gateway_response}')
    return api_gateway_response

def get_category_totals(transactions_data):
    user_categories = ['fun', 'unpredictable_necessities', 'predictable_necessities', 'other']
    category_totals = {}
    for user_category in user_categories:
        category_totals[user_category] = calculate_category_total(user_category, transactions_data)
    print(f'category_totals: {category_totals}')
    return category_totals

def calculate_category_total(user_category, transactions_data):
    category_amounts = extract_category_amounts_from_plaid_transactions_get(transactions_data, user_category)
    category_total = add_dollar_amounts(category_amounts)
    print(f'user_category: {user_category} | category_total: {category_total}')
    return category_total

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

def extract_category_amounts_from_plaid_transactions_get(payload_plaid_transactions_get, user_category):
    print(f'Made it to extract_dollar_amounts_from_plaid_transactions_get')
    amounts = []
    transactions = payload_plaid_transactions_get['transactions']
    for transaction in transactions:
        transaction_category = get_transaction_user_category(transaction)
        if transaction_category == user_category:
            amount = transaction['amount']
            amounts.append(amount)
    print(f'amounts in user_category {user_category}: {amounts}')
    return amounts

def get_transaction_user_category(transaction):
    print(f'Made it to get_transaction_user_category')
    my_credit_card_account_id = 'eO50JxE95whkXAVjg7nZu4zJ4ynKjMCdbXen0'
    user_category_of_transaction = ''
    with open('src/category_mappings.json', 'r') as f:
        category_mappings = json.load(f)
    if transaction['account_id'] == my_credit_card_account_id and 'Payment' not in transaction['category']:
        primary_transaction_category = transaction['category'][0]
        secondary_transaction_category = transaction['category'][1] if len(transaction['category']) > 1 else ''
        if primary_transaction_category == 'Shops' and secondary_transaction_category == 'Supermarkets and Groceries':
            user_category_of_transaction = 'predictable_necessities'
        elif primary_transaction_category == 'Travel' and secondary_transaction_category =='Gas Stations':
            user_category_of_transaction = 'predictable_necessities'
        else:
            user_category_of_transaction = category_mappings[primary_transaction_category]
    print(f'transaction_id: {transaction["transaction_id"]} | user_category_of_transaction: {user_category_of_transaction}')
    return user_category_of_transaction

def add_dollar_amounts(dollar_amounts):
    print(f'Made it to add_dollar_amounts')
    total = 0
    for amount in dollar_amounts:
        amount = float(str(amount).replace('$', '').replace(',', ''))
        total = total + amount
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

def get_todays_date():
    return str(datetime.date.today())

def get_last_thursday_date():
    today = datetime.date.today()
    offset = (today.weekday() - calendar.THURSDAY) % 7
    last_thursday_date = str(today - datetime.timedelta(days=offset))
    print(f'last_thursday_date: {last_thursday_date}')
    return last_thursday_date