import ftplib
from os import listdir as os_listdir, remove as os_remove
from os.path import isfile as os_isfile
from config import ftp

def set_cwd(ftp_client: ftplib.FTP, target_dir: str):
  if target_dir != '':
    try:
      ftp_client.cwd(target_dir)
    except ftplib.error_perm:
      set_cwd(ftp_client, '/'.join(target_dir.split('/')[:-1]))
      ftp_client.mkd(target_dir)
      ftp_client.cwd(target_dir)

def transfer_tracks(playlist_id: str):
  base_dir = f'downloads/{playlist_id}'
  ftp_destination = ftp['path'] + f'/{playlist_id}/'
  transfer_count = 0
  for file in os_listdir(base_dir):
    filename = f'{base_dir}/{file}'
    if os_isfile(filename) and file != '' and file[0] != '.' and '.spotdlTrackingFile' not in file:
      transfer_count += 1
      print(f'[FTP] transferring file "{file}"')
      with open(filename, 'rb') as fp:
        with ftplib.FTP(host=ftp['host'], user=ftp['user'], passwd=ftp['pwd']) as ftp_client:
          set_cwd(ftp_client, ftp_destination)
          ftp_client.storbinary(f'STOR {file}', fp)

      os_remove(filename)
  
  print(f'[FTP] transferred {transfer_count} track(s) for playlist {playlist_id}')
