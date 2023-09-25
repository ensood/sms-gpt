import logging
import json
from typing import NamedTuple

def config_log(log_file_name: str = 'base.log', log_level: int = logging.INFO, log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s') -> None:
    # Configure logging
    logging.basicConfig(
        filename = log_file_name,
        level = log_level,
        format = log_format
    )

class Credentials(NamedTuple):
    available: bool
    openai_api_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

def config_credentials() -> Credentials:
    # Load credentials configuration
    with open('helpers/configuration/config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    try:
        openai_api_key = config['openai_api_key']
        twilio_account_sid = config['twilio_account_sid']
        twilio_auth_token = config['twilio_auth_token']
        twilio_phone_number = config['twilio_phone_number']
        available = True
        credentials = Credentials(available, openai_api_key, twilio_account_sid, twilio_auth_token, twilio_phone_number)
    except KeyError as keys_error:
        logging.error('Error: %s', str(keys_error))
        credentials = Credentials(False, '', '', '', '')
    finally:
        return credentials