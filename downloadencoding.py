import requests
import os

storage_url=’https://firebasestorage.googleapis.com/v0/b/nodemc-9edd3.appspot.com/o/EncodeFile.p?alt=media’
des_dir = '/home/pi4/Desktop/security_system'

def download_encodings(storage_url, destination_directory):
response = requests.get(storage_url)
if response.status_code == 200:

Extract the filename from the response headers
content_disposition = response.headers.get('Content-Disposition')
if content_disposition and 'filename=' in content_disposition:
file_name = content_disposition.split('filename=')[1].strip('"')
else:
file_name = 'downloaded_file'

destination_file_path = os.path.join(destination_directory, file_name)

with open(destination_file_path, 'wb') as file:
    file.write(response.content)

print(f'Successfully downloaded file: {destination_file_path}')
else:
print('Failed to download file.')

download_encodings(storage_url,des_dir)
