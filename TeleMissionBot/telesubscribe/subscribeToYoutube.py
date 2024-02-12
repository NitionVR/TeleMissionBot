#Uses youtube api to log in to user account (auth)
#then check list the channels they are subscribed to the specified channel
#if they are not already subcribed.

from ...TeleMissionBot.util import util
import google_auth

TOKEN_PATH = 'token.json'
CLIENT_SECRET_PATH = util.get_paths_to_config('config','credentials.json','token.json')

if __name__ == '__main__':
    google_auth.authenticate_user(CLIENT_SECRET_PATH,TOKEN_PATH)