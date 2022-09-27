from dotenv import load_dotenv
from os import getenv as os_getenv, system as os_system
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import json

load_dotenv()
config = {
  'spotify': {
  'client_id': os_getenv('SPOTIFY_CLIENT_ID'),
  'client_secret': os_getenv('SPOTIFY_CLIENT_SECRET'),
  'redirect_uri': os_getenv('SPOTIFY_REDIRECT_URI')
  }
}

track_link = lambda id : f'https://open.spotify.com/track/{id}'
playlist_id = '1cXTRvIX0gssOrTALbwpKO'

sp = Spotify(auth_manager=SpotifyOAuth(
  client_id=config['spotify']['client_id'],
  client_secret=config['spotify']['client_secret'],
  redirect_uri=config['spotify']['redirect_uri']
))

def load_process_log():
  log = {}
  try:
    with open('proclog.txt', 'r') as f:
      log = json.loads(f.read())
  except FileNotFoundError:
    with open('proclog.txt', 'w') as f:
      f.write('{}')
  return log

def save_process_log(log):
  try:
    with open('proclog.txt', 'w') as f:
      f.write(json.dumps(log))
    return True
  except:
    return False

def get_playlist_items(id, skip):
  return sp.playlist_items(id, limit=100, offset=skip)['items']

def process_playlist(id):
  proclog = load_process_log()
  skip = 0
  items = get_playlist_items(id, skip)
  while len(items) > 0:
    for item in items:
      track_id = item['track']['id']
      track_name = item['track']['name']
      try:
        exists = proclog[track_id]
        print(f'[SKIP] {track_name}')
        continue
      except KeyError:
        pass

      # Run spotdl
      print(f'[ DL ] {track_name}')
      os_system(f'venv/bin/spotdl {track_link(track_id)} --output downloads/')

      proclog[track_id] = {
        'name': track_name,
        'album': item['track']['album']['name'],
        'track_num': item['track']['track_number'],
        'added': item['added_at']
      }
      save_process_log(proclog)
        
    skip += 100
    items = get_playlist_items(id, skip)

try:
  process_playlist(playlist_id)
except KeyboardInterrupt:
  print('\nuser terminated process\n')
