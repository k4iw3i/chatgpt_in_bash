import requests
import json
import os
import sys
import time
import threading
from utils import *
from rich.console import Console
from rich.markdown import Markdown
from utils import loading_texts
import random
import math

class ChatBot:
    def __init__(self ) -> None:
        self.url = "https://api.openai.com/v1/chat/completions"
        self._get_config()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.messages = [{"role": "system", "content": self.bot_setting}]
        self._equalize_name()
        self.converse()

    def _equalize_name(self):

        self.user_name = "You"
        you_len = len(self.user_name)
        bot_len = len(self.bot_name)
        diff = abs(you_len - bot_len)
        if you_len > bot_len:
            self.bot_name = math.ceil((diff)/2) * " " + self.bot_name + " " * math.floor((diff)/2)
        elif you_len < bot_len:
            self.user_name = math.ceil((diff)/2) * " " + self.user_name + " " * math.floor((diff)/2)
        
        
    def _get_config(self):
        script_path = "/".join(os.path.abspath(sys.argv[0]).split('/')[:-1])
        try:
            with open(f"{script_path}/bot_config.json", "r") as f:
                config = json.load(f)
                self.token = config["api_key"]
                self.bot_name = config["bot_name"]
                self.bot_setting = config["bot_setting"]
                self.model = config["model"]
        except:
            print ("First time running, please configure your bot.")
            os.system("python configure.py")
        
    def converse(self):
        _continue = True
        while _continue:
            _message = input(f"{BOLD}{self.user_name}{RESET}: ")
            if _message in exit_texts:
                self._exit()
            print ()
            self.messages.append({"role": "user", "content": _message})
            payload = {
                'model': self.model,
                'messages': self.messages,
            }

            self.reply(payload)
            print()

    def reply(self, payload):
        stop_event = threading.Event() 
        loading_thread = threading.Thread(target=self.loading_animation, args=(stop_event,)) 
        loading_thread.start()
        response = requests.post(self.url, headers=self.headers, data = json.dumps(payload))
        stop_event.set()
        try:
            _response = response.json()['choices'][0]['message']['content']
            self.load_markdown(_response)
            self.messages.append(response.json()['choices'][0]['message'])
        except:
            print (f"\r{GREEN}{BOLD}{self.bot_name}{RESET}: Something is wrong, please call Elon Musk.")
            print (response.text)


    def loading_animation(self, stop_event):
        animation = "|/-\\"
        idx = 0
        loading_text = random.choice(loading_texts)
        while not stop_event.is_set():
            sys.stdout.write(f'\r{GREEN}{BOLD}{self.bot_name}{RESET}: ' + loading_text + " " + animation[idx % len(animation)])
            idx += 1
            time.sleep(0.1)

    def load_markdown(self, markdown_string):
        console = Console()
        markdown = Markdown(markdown_string)
        sys.stdout.write (f"\r{GREEN}{BOLD}{self.bot_name}{RESET}: ")
        console.print(markdown)

    def _exit(self):
        for i in range (3):
            print (f"\r{GREEN}{BOLD}{self.bot_name}{RESET}: Hibernating in {3-i}...", end="")
            time.sleep(1)
        exit()

if __name__ == "__main__":
    chatbot = ChatBot()