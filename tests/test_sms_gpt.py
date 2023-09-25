import unittest
from unittest.mock import Mock
import helpers.sms_gpt as sg

class TestSMSGPT(unittest.TestCase):

    def setUp(self):
        self.ai_service = Mock()
        self.twilio_service = Mock()
        self.sms_gpt = sg.SMSGPT(self.ai_service, self.twilio_service)

    def test_process_sms(self):
        from_number = '1234567890'
        body = 'test message'

        self.ai_service.process_message.return_value = 'a generated response'
        self.twilio_service.send_sms.return_value = None

        self.sms_gpt.process_sms(from_number, body)

        self.ai_service.process_message.assert_called_once_with(body, False)
        self.twilio_service.send_sms.assert_called_once_with(from_number, 'a generated response')

    def test_create(self):
        ai_service = Mock()
        twilio_service = Mock()

        sms_gpt = sg.create(ai_service, twilio_service)

        self.assertIsInstance(sms_gpt, sg.SMSGPT)
        self.assertEqual(sms_gpt.ai_service, ai_service)
        self.assertEqual(sms_gpt.twilio_service, twilio_service)

if __name__ == '__main__':
    unittest.main()
