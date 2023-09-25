import logging
from twilio.rest import Client

class TwilioService:
    """
    A service for sending SMS using Twilio.
    """
    def __init__(self, account_sid: str, auth_token: str, phone_number: str) -> None:
        """
        Initialize the Twilio service.

        Args:
            account_sid (str): Twilio account SID.
            auth_token (str): Twilio authentication token.
            phone_number (str): your Twilio phone number.
        """
        self.phone_number = phone_number
        try:
            self.client = Client(account_sid, auth_token)
        except Exception as error_init_twilio:
            logging.error('Error: %s', str(error_init_twilio))

    def send_sms(self, to_number: str, message: str) -> None:
        """
        Send an SMS message using Twilio.

        Args:
            to_number (str): The recipient's phone number.
            message (str): The message to send.
        """
        self.client.messages.create(
            to=to_number,
            from_=self.phone_number,
            body=message
        )

    def get_stats(self, lastest_msgs_count: int) -> tuple:
        """
        Get stats for SMS messages.

        Returns:
            tuple: A tuple containing the total number of messages and the list of lastest messages.
        
        """
        messages = self.client.messages.list()
        message_content = [message.body for message in messages]
        return len(message_content), message_content[-lastest_msgs_count:]

def create(account_sid, auth_token, phone_number):
    """
    Creates a new instance of the TwilioService class with the given Twilio credentials.
    """
    twilio_service = TwilioService(account_sid, auth_token, phone_number)
    return twilio_service
