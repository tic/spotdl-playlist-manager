import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from os import system as os_system, makedirs as os_makedirs
from os.path import dirname as os_dirname
from platform import system as platform_system

from config import spotify

sp = Spotify(auth_manager=SpotifyOAuth(
  client_id=spotify['client_id'],
  client_secret=spotify['client_secret'],
  redirect_uri=spotify['redirect_uri']
))

track_link = lambda id : f'https://open.spotify.com/track/{id}'

def load_process_log(playlist_id):
  log = {}
  file = f'log/{playlist_id}.json'
  os_makedirs(os_dirname(file), exist_ok=True)

  try:
    with open(file, 'r') as f:
      log = json.loads(f.read())
  except FileNotFoundError:
    with open(file, 'w') as f:
      f.write('{}')
  return log

def save_process_log(playlist_id: str, log: dict):
  try:
    with open(f'log/{playlist_id}.json', 'w') as f:
      f.write(json.dumps(log, indent=2))
    return True
  except:
    return False

def dispatch_spotdl(playlist_id: str, track_id: str):
  download_dir = f'downloads/{playlist_id}/'
  os_makedirs(os_dirname(download_dir), exist_ok=True)

  executable = 'python venv\Lib\site-packages\spotdl\__main__.py' if platform_system() == 'Windows' else 'venv/bin/spotdl'

  try:
    os_system(f'{executable} {track_link(track_id)} --output {download_dir} --ignore-ffmpeg-version')
    return True
  except Exception:
    return False

def get_playlist_items(id):
  all_items = []
  offset = 0

  items = sp.playlist_items(id, limit=100, offset=offset)['items']
  while len(items) > 0:
    all_items.extend(items)
    print(f'[PL] scanned {len(all_items)} items')
    offset += 100
    items = sp.playlist_items(id, limit=100, offset=offset)['items']
  
  return all_items

# Returns a list of track ids that have been added since the last check
def detect_changes(process_log: dict, playlist_id: str):
  playlist_items = get_playlist_items(playlist_id)
  new_items = []
  for item in playlist_items:
    try:
      if item['track']['id'] is not None:
        process_log[item['track']['id']]
    except KeyError:
      new_items.append(item)

  return new_items


def check_for_new_items(playlist_id: str):
  print(f'[PL] scanning {playlist_id}')
  process_log = load_process_log(playlist_id)
  new_items = detect_changes(process_log, playlist_id)
  for item in new_items:
    track_id = item['track']['id']
    track_name = item['track']['name']
    print(f'[PL] {playlist_id} --> new item "{track_name}"')
    process_log[track_id] = {
      'name': track_name,
      'album': item['track']['album']['name'],
      'track_num': item['track']['track_number'],
      'added': item['added_at']
    }

    dispatch_success = dispatch_spotdl(playlist_id, track_id)

    if dispatch_success:
      save_process_log(playlist_id, process_log)
    
  return len(new_items)
