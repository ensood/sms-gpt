import unittest
from unittest.mock import Mock
from helpers.twilio_handler import TwilioService

class TestTwilioService(unittest.TestCase):

    def setUp(self):
        # Create a mock Twilio client for testing
        self.mock_client = Mock()
        self.account_sid = "your_account_sid"
        self.auth_token = "your_auth_token"
        self.phone_number = "your_phone_number"

        self.twilio_service = TwilioService(self.account_sid, self.auth_token, self.phone_number)
        self.twilio_service.client = self.mock_client

    def test_send_sms(self):
        to_number = "12223334444"
        message = "message"
        self.twilio_service.send_sms(to_number, message)
        self.mock_client.messages.create.assert_called_once_with(
            to=to_number,
            from_=self.phone_number,
            body=message
        )

    def test_get_stats(self):
        # Create some mock messages
        mock_message_list = [Mock(body=f"message{i}") for i in range(5)]
        self.mock_client.messages.list.return_value = mock_message_list

        total_messages, latest_messages = self.twilio_service.get_stats(3)

        self.assertEqual(total_messages, 5)
        self.assertEqual(len(latest_messages), 3)
        self.assertEqual(latest_messages, ["message2", "message3", "message4"])

if __name__ == '__main__':
    unittest.main()
