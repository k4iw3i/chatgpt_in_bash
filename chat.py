import requests
import json
import os
import sys

class ChatBot:
    def __init__(self, setting) -> None:
        self.setting = setting
        self.url = "https://api.openai.com/v1/chat/completions"
        self.token = self._get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.messages = [{"role": "system", "content": setting}]
        

    def _get_token(self):
        try:
            return os.environ["PERSONAL_OPENAI_KEY"]
        except:
            print ("Please enter your OpenAI API key: ")
            os.environ['PERSONAL_OPENAI_KEY'] = input()
            return os.environ["PERSONAL_OPENAI_KEY"]
        
    def converse(self):
        _continue = True
        while _continue:
            _message = input("You: ")
            if _message == "exit":
                _continue = False
                break
            self.messages.append({"role": "user", "content": _message})
            payload = {
                'model': 'gpt-3.5-turbo',
                'messages': self.messages,
            }
            response = requests.post(self.url, headers=self.headers, data = json.dumps(payload))
            _response = response.json()['choices'][0]['message']['content']
            print (f"AI: {_response}")
            self.messages.append(response.json()['choices'][0]['message'])

    def loading_spinner():
        spinner_characters = "|/-\\"
        spinner_index = 0

        while not request_done.is_set():
            sys.stdout.write("\rWaiting for response... " + spinner_characters[spinner_index])
            sys.stdout.flush()
            spinner_index = (spinner_index + 1) % len(spinner_characters)
            time.sleep(0.1)

        sys.stdout.write("\r")  # Clear the current line
        sys.stdout.flush()