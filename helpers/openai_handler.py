import logging
import openai
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class AIService:
    """
    A service for interacting with the OpenAI API.
    """
    def __init__(self, openai_api_key: str) -> None:
        """
        Initialize the AI service.

        Args:
            openai_api_key (str): The API key for OpenAI.
        """
        openai.api_key = openai_api_key
        self.openai_model = 'gpt-3.5-turbo'
        self.openai_max_token = 150
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    def __reduce_prompt_chars(self, message: str) -> str:
        """
        Private func to reduce message chars to reduce cost of api.

        Args:
            message (str): The user's message.

        Returns:
            str: message without stopwords.
        """
        tokens = word_tokenize(message)
        filtered_tokens = (word for word in tokens if word.lower() not in self.stop_words)
        processed_message = ' '.join(filtered_tokens)

        logging.info('Reduced prompt chars from %d to %d', len(message), len(processed_message))

        return processed_message
    
    def config(self, model: str, max_token: int) -> None:
        """
        Configure the OpenAI model and max token.

        Args:
            model (str): The model to use.
            max_token (int): The maximum number of tokens to use.
        """
        self.openai_model = model
        self.openai_max_token = max_token

    def process_message(self, message: str, reduce_token_cost: bool) -> str:
        """
        Process the user's message using OpenAI.

        Args:
            message (str): The user's message.
            reduce_token_cost (bool): Whether to reduce token cost by removing stopwords.

        Returns:
            str: The AI-generated response.
        """

        processed_message = self.__reduce_prompt_chars(message) if reduce_token_cost else message

        try:
            response = openai.ChatCompletion.create(
                model = self.openai_model,
                messages = [{'role': 'user', 'content': str(processed_message)}],
                max_tokens = self.openai_max_token
            )
            logging.info('Successfully got OpenAI response.')
            return response.choices[0].message.content
        except Exception as unknown_error:
            logging.error('Error on openai: %s', str(unknown_error))
            return 'System error, please try again later.'

def create(openai_api_key):
    """
    Creates a new instance of the AIService class with the given OpenAI API key.
    """
    ai_service = AIService(openai_api_key)
    return ai_service
