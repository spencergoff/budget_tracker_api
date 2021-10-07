import os
import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world(event, context):
    body = 'Hello, world!'
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }

def running_in_aws_lambda():
    if os.environ.get('AWS_EXECUTION_ENV') == None:
        return False
    else:
        return True

if __name__ == '__main__':
    if not running_in_aws_lambda():
        print('Not running in Lambda')
        app.run(host='0.0.0.0', port=5000)
    else:
        print('Running in Lambda')