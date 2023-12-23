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

