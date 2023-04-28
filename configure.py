import json
from utils import *
import sys
import os

def main():
    script_path = "/".join(os.path.abspath(sys.argv[0]).split('/')[:-1])

    api_key = input("Please enter your OpenAI API key: \n")

    bot_name = input("\nHow do you want to call your bot?\n")

    bot_setting = input("\nPlease define your bot: \n")
    bot_setting += f"Your name is {bot_name}"

    print ("\nSelect a model\n1. gpt-3.5-turbo (default)")
    selection = input("\nYour selection: ")
    models = {
        '1': 'gpt-3.5-turbo'
    }
    model = models[selection]

    print ("Setting up your bot...")
    with open(f"{script_path}/bot_config.json", "w") as f:
        config = {
            "api_key": api_key,
            "bot_name": bot_name,
            "bot_setting": bot_setting,
            "model": model
        }
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    main()