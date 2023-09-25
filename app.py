import logging

from flask import Flask, request, abort, jsonify
from helpers import openai_handler, twilio_handler, sms_gpt
from helpers.configuration.config import config_log, config_credentials, Credentials

app = Flask(__name__)

# Configurations:
config_log(log_file_name='base.log', log_level=logging.INFO)
credentials = Credentials(*(config_credentials()))

# Initialize services and inject dependencies
if credentials.available:
    openai_handler = openai_handler.create(credentials.openai_api_key)
    twilio_handler = twilio_handler.create(
        credentials.twilio_account_sid,
        credentials.twilio_auth_token,
        credentials.twilio_phone_number
    )
    sms_gpt = sms_gpt.create(openai_handler, twilio_handler)

# root route
@app.route('/', methods=['GET'])
def index():
    return 'Welcome to SMS GPT!', 200

# hook for Twilio to get SMS
@app.route('/sms', methods=['POST'])
def receive_sms():
    from_number = request.form['From']
    body = request.form['Body']
    sms_gpt.process_sms(from_number, body, reduce_token_cost=True)

    return '', 204

# stats route
@app.route('/sms-stat', methods=['GET'])
def stats():
    try:
        # Validate query parameters
        if request.args.get('n') is not None:
            n = request.args.get('n')
        else:
            abort(400, 'Missing n parameter')

        if n.startswith('-') or not n.isnumeric():
            abort(400, 'Invalid number of messages requested')
        
        total_count, selected_msgs = twilio_handler.get_stats(int(n))
        response = {
            'message_count': total_count,
            f'list_of_last_{n}_messages': selected_msgs
        }

        return jsonify(response), 200

    except Exception as internal_error:
        logging.error('Error: %s', str(internal_error))
        abort(500, 'Internal Server Error!')


if __name__ == '__main__':
    if credentials.available:
        app.run(host='localhost', port=5000, debug=True)
    else:
        logging.error('Error: Missing API keys!')
        print('First, set your API keys in config.json to run the app.')
