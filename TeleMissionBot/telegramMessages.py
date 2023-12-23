import configparser
import json
import asyncio
from datetime import date, datetime, timedelta

from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)


#Read config file
config = configparser.ConfigParser()
config.read("config.ini")


