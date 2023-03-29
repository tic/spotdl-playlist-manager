from dotenv import load_dotenv
from os import getenv as os_getenv
load_dotenv()

spotify = {
  'client_id': os_getenv('SPOTIFY_CLIENT_ID'),
  'client_secret': os_getenv('SPOTIFY_CLIENT_SECRET'),
  'redirect_uri': os_getenv('SPOTIFY_REDIRECT_URI'),
}

playlist_ids = os_getenv('SPOTIFY_PLAYLIST_IDS').split(',')

ftp = {
  'host': os_getenv('FTP_HOST'),
  'user': os_getenv('FTP_USERNAME'),
  'pwd': os_getenv('FTP_PWD'),
  'path': os_getenv('FTP_PATH'),
}
