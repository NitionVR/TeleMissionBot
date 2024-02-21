from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from ..util import util
from . import google_auth
import os.path
from urllib.parse import urlparse, parse_qs

TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'config/credentials.json'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def build_service(creds):
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def get_channel_id_from_username(youtube, username):
    response = youtube.channels().list(part='id',forUsername=username).execute()

    if 'items' in response:
        return response['items'][0]['id']
    else:
        return None

def extract_username_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    if '@' in path_parts[-1]:
        return path_parts[-1].replace('@', '')
    else:
        return None

def check_and_subscribe(creds, channel_url):
    youtube = build_service(creds=creds)

    username = extract_username_from_url(channel_url)

    if username is None:
        print("Invalid YouTube channel URL.")
        return

    channel_id = get_channel_id_from_username(youtube, username)

    if channel_id is None:
        print(f"Could not find a channel ID for the username: {username}")
        return

    subscriptions = youtube.subscriptions().list(part='snippet', mine=True).execute()

    for subscription in subscriptions['items']:
        if subscription['snippet']['resourceId']['channelId'] == channel_id:
            print(f"Already subscribed to {username}.")
            return

    youtube.subscriptions().insert(
        part='snippet',
        body={'snippet': {'resourceId': {'kind': 'youtube#channel','channelId': channel_id}}}).execute()

    print(f"Subscribed to the {username}.")

if __name__ == '__main__':
    creds, access_token = google_auth.authenticate_user(CREDENTIALS_PATH, TOKEN_PATH)
    specified_channel_url = 'https://www.youtube.com/@RockstarGames'
    check_and_subscribe(creds, specified_channel_url)
