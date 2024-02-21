import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
]

TOKEN_PATH = 'config/token.json'
CLIENT_SECRET_PATH = 'config/credentials.json'

def authenticate_user(client_secret_path, token_path):
    """
    Authenticates the user and returns the credentials.

    :param client_secret_path: Path to the client secret file.
    :param token_path: Path to the token file.
    :return: Tuple containing credentials and access token.
    """
    creds = load_existing_credentials(token_path)
    if not creds or not creds.valid:
        creds = start_authentication_flow(client_secret_path, token_path)
        access_token = creds.token
    else:
        access_token = creds.token
    return creds, access_token


def get_user_info(access_token):
    """
    Gets the JSON response format of user information by sending a request
    to the userinfo endpoint of the Google API.

    :param access_token: Access token obtained during authentication.
    :return: User information in JSON format.
    """
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        print(f"An error occurred: {response.status_code}")
        return None


def extract_user_info(user_info):
    """
    Extracts the email and Google user ID from the JSON file of user information.

    :param user_info: User information in JSON format.
    :return: Tuple containing Google user ID and email address.
    """
    if user_info:
        google_user_id = user_info.get('id')
        email_address = user_info.get('email')
        return google_user_id, email_address
    return None


def start_authentication_flow(client_secret_path, token_path):
    """
    Initializes the Google Auth 2.0 flow.

    :param client_secret_path: Path to the client secret file.
    :param token_path: Path to the token file.
    :return: Google API credentials.
    """
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)

    creds = flow.run_local_server(port=0)

    if sorted(SCOPES) != sorted(creds.scopes):
        print('Warning: Requested and granted scopes do not match.')
    save_credentials(creds, token_path)

    return creds


def save_credentials(credentials, token_path):
    """
    Saves credentials to a token file.

    :param credentials: Google API credentials.
    :param token_path: Path to the token file.
    :return: None
    """
    with open(token_path, 'w') as token_file:
        token_file.write(credentials.to_json())


def load_existing_credentials(token_path):
    """
    Loads and returns credentials if they already exist.

    :param token_path: Path to the token file.
    :return: Google API credentials if valid, else None.
    """
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        return creds if creds.valid else None
    return None

