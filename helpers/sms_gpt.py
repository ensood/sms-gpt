import logging

class SMSGPT:
    """
    A class that to process SMS messages and to provide response with AI.
    """

    def __init__(self, ai_service: object, twilio_service: object) -> None:
        """
        Initialize the SMS GPT service.

        Args:
            ai_service (object): An instance of AIService.
            twilio_service (object): An instance of TwilioService.
        """
        self.ai_service = ai_service
        self.twilio_service = twilio_service

    def process_sms(self, from_number: str, body: str, reduce_token_cost: bool = False) -> None:
        """
        Process a SMS message and send a response.

        Args:
            from_number (str): The sender's phone number.
            body (str): The message body.
        """
        logging.info('Received SMS from %s: %s', from_number, body)
        ai_response = self.ai_service.process_message(body, reduce_token_cost)
        self.twilio_service.send_sms(from_number, ai_response)
        logging.info('Response sent to %s: %s', from_number, ai_response)


def create(ai_service, twilio_service):
    """
    Creates a new instance of the SMSGPT class with the given AI and Twilio objects.
    """
    sms_gpt = SMSGPT(ai_service, twilio_service)
    return sms_gpt
