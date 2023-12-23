import configparser
import json
import asyncio
import aiofiles
from datetime import date, datetime, timedelta
from typing import Any

from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

CONFIG_SECTION = "Telegram"
API_ID_KEY = "api_id"
API_HASH_KEY = "api_hash"
PHONE_NUMBER_KEY = "phone_number"
USER_NAME_KEY = "username"
CONFIG_FILE = "config.ini"

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        
        if isinstance(o,bytes):
            return list(o)
        
        return json.JSONEncoder.default(self,o)

def config_file():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def configure_api(config):
    api_id = config[CONFIG_SECTION][API_ID_KEY]
    api_hash = str(config[CONFIG_SECTION][API_HASH_KEY])
    return (api_id,api_hash)


def configure_user(config):
    phone_number = config[CONFIG_SECTION][PHONE_NUMBER_KEY]
    username = config[CONFIG_SECTION][USER_NAME_KEY]
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
    

async def get_channel():
    while True:
        try:
            entity = get_channel_info()
            my_channel = await client.get_entity(entity)
            return my_channel
        except ValueError:
            continue

async def fetch_messages(client, my_channel, offset_id, limit):
    return await client(GetHistoryRequest(
        peer=my_channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0,
    ))

async def process_messages(messages, total_messages, total_count_limit, all_messages):
    if not messages:
        return False

    for message in messages:
        all_messages.append(message.to_dict())
        offset_id = messages[-1].id
        total_messages = len(all_messages)

        if total_count_limit != 0 and total_messages >= total_count_limit:
            return False

    return True

async def get_messages(client, my_channel):
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print(f"Current Offset ID is: {offset_id}; Total Messages: {total_messages}")

        history = await fetch_messages(client, my_channel, offset_id, limit)
        if not await process_messages(history.messages, total_messages, total_count_limit, all_messages):
            break

    return all_messages

                               
async def store_messages(messages,filename = "telegram_messages.json"):
    async with aiofiles.open(filename,"w") as outfile:
        await json.dump(messages, outfile, cls = DateTimeEncoder)

async def main(client):
    
    await client.start()
    print("Client Created")

    await authorize_client(client,PHONE_NUMBER_KEY)
    me = await client.get_me()
    
    my_channel = await get_channel()

    messages = await get_messages(client,my_channel)

    await store_messages(messages)


if __name__ == "__main__":
    client = create_client()
    with client:
        client.loop.run_until_complete(main(client))