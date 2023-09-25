import unittest
from unittest.mock import patch
from helpers.openai_handler import AIService

class TestAIService(unittest.TestCase):
    def setUp(self):
        self.openai_api_key = 'your_api_key_here'
        self.ai_service = AIService(self.openai_api_key)

    def test_config(self):
        # Test configuring the OpenAI service.
        self.ai_service.config('davinci-002', 999)
        self.assertEqual(self.ai_service.openai_model, 'davinci-002')
        self.assertEqual(self.ai_service.openai_max_token, 999)

    def test_process_message_without_reducing_token_cost(self):
        # Test processing a message without reducing token cost.
        message = "how are you?"
        response = self.ai_service.process_message(message, reduce_token_cost=False)
        self.assertIsInstance(response, str)

    @patch('helpers.openai_handler.openai.ChatCompletion.create')
    def test_process_message_with_reducing_token_cost(self, mock_openai_create):
        # Test processing a message with reducing token cost using a mock response.
        message = "how are you?"
        mock_openai_create.return_value.choices[0].message.content = "fine!"
        response = self.ai_service.process_message(message, reduce_token_cost=True)
        self.assertEqual(response, "fine!")

    @patch('helpers.openai_handler.openai.ChatCompletion.create', side_effect=Exception("an error"))
    def test_process_message_error_handling(self, mock_openai_create):
        # Test error handling when processing a message.
        message = "how are you?"
        response = self.ai_service.process_message(message, reduce_token_cost=False)
        self.assertEqual(response, 'System error, please try again later.')

if __name__ == '__main__':
    unittest.main()
