from time import sleep
import print as cprint
from config import playlist_ids
from spotify import check_for_new_items
from ftp import transfer_tracks

def event_loop():
  print(f'[EL] starting event loop')
  for playlist_id in playlist_ids:
    update_count = check_for_new_items(playlist_id)
    if update_count > 0:
      transfer_tracks(playlist_id)

def main():
  try:
    if len(playlist_ids) == 0:
      print('[WARN] no playlists configured -- exiting')
      return

    while True:
      event_loop()
      sleep(600)
  except KeyboardInterrupt:
    print('user terminated process\n')

if __name__ == '__main__':
  main()
