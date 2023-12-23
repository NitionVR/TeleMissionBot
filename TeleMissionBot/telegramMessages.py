import configparser
import json
import asyncio
from datetime import date, datetime, timedelta

from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)


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

