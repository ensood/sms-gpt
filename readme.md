# SMS based assistant with OpenAI and Twilio

## Overview

This is a simple SMS assistant project that utilized the OpenAI API and Twilio to provide automated responses to incoming text messages with AI-generated text.

## High-level System Overview

<p align="center">
  <img src="https://github.com/ensood/sms-gpt/blob/main/system.png" alt="High-level System Overview">
</p>

This diagram provides a high-level view of my system, showcasing the interactions between various components.      

- Client: Where users send text messages.   
- Twilio: The communication gateway that forwards messages to our system and from our system to clients.   
- Flask App: Our central processing hub.   
- OpenAI API: create generative responses.    

Messages flow from the client to Twilio, then to our Flask app for pre-processing, then using the OpenAI API for generative response. Finally, responses are sent back to user through Twilio and via SMS.

## Features

- Utilizes the OpenAI API to generate AI responses based on user messages.
- Sends SMS responses using the Twilio service.
- Reduces token cost by removing stopwords from input messages using nltk.
- Logs incoming messages and responses for monitoring and troubleshooting.

## Setup

To run this project locally, you'll need to:

1. Obtain API keys and credentials for OpenAI and Twilio.
2. Set up a Python environment with the required dependencies; use requirments.txt
3. API keys and credentials should be stored securely and loaded from environment variables.  
   NOTE: For simplicity, configure your API keys and credentials in the `configuration/config.json` file.
4. Setup webhook for text messages in Twilio console; ex. yourdomain.com/sms  
   NOTE: For test, use ngrok to setup a local http server with exposer to the internet
5. Start the Flask application using `python app.py`.

## Usage

1. Send an SMS to the provided Twilio phone number.
2. The code will process the message, generate a response, and send it back to you as an SMS.
3. You can monitor logs in `your_log_file.log` file for debugging and system status.
4. You can adjust the OpenAI model and max_token in the `openai_handler.config()`.


## Test Report:

```Coverage Table:
Name                              Stmts   Miss  Cover
-----------------------------------------------------
app.py                               39     12    69%
helpers/configuration/config.py      25      3    88%
helpers/openai_handler.py            34      0   100%
helpers/sms_gpt.py                   13      0   100%
helpers/twilio_handler.py            18      2    89%
tests/__init__.py                     0      0   100%
tests/test_app.py                    19      4    79%
tests/test_openai_handler.py         28      1    96%
tests/test_sms_gpt.py                25      1    96%
tests/test_twilio_handler.py         25      1    96%
-----------------------------------------------------
TOTAL                               226     24    89%
```
