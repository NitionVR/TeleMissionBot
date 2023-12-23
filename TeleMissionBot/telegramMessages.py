import configparser
import json
import asyncio
from datetime import date, datetime, timedelta
from typing import Any

from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        
        if isinstance(o,bytes):
            return list(o)
        
        return json.JSONEncoder.default(self,o)

def config_file():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def configure_api(config):
    api_id = config["Telegram"]["api_id"]
    api_hash = str(config["Telegram"]["api_hash"])
    return (api_id,api_hash)


def configure_user(config):
    phone_number = config["Telegram"]["phone_number"]
    username = config["Telegram"]["username"]
    return (phone_number,username)


def create_client():
    config = config_file()
    api_id,api_hash = configure_api(config)
    username = configure_user(config)[1]

    client = TelegramClient(username,api_id,api_hash)
    return client


async def authorize_client(client, phone_number):
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone_number)
        print("A verification code has been sent to your cellphone number.")
        try:
            await client.sign_in(phone_number, input("Enter the code: "))
        except SessionPasswordNeededError:
            await client.sign_in(password=input("Enter password: "))


def get_channel_info():
    user_channel = input("Enter Telegram channel URL or ID: ").strip()

    try:
        if user_channel.isdigit():
            entity = PeerChannel(int(user_channel))
        else:
            entity = user_channel
    except ValueError:
        print("Invalid input. Please enter a valid Telegram channel URL or ID")
        return None
    
    return entity
    

async def get_messages(client,my_channel):
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print(f"Current Offset ID is: {offset_id}; Total Messages: {total_messages}")
        history = await client(GetHistoryRequest(
            peer = my_channel,
            offset_id = offset_id,
            offset_date = None,
            add_offset = 0,
            limit = limit,
            max_id = 0,
            min_id = 0,
            hash = 0,
        ))

        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
            offset_id = messages[len(messages)-1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

                                 
def store_messages(messages,filename = "telegram_messages.json"):
    with open(filename,"w") as outfile:
        json.dump(messages, outfile, cls = DateTimeEncoder)