import requests
import os
from pymongo import MongoClient
import re

# def get_google_drive_link():
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client.Mecha  # Database name
#     collection = db.photo  # Collection name

#     # Fetch the most recently added document
#     photo_data = collection.find().sort('_id', -1).limit(1).next()
#     return photo_data['file_url']  # Assuming the URL is saved under 'file_url'

url = "https://drive.google.com/file/d/1g0KcgaGmOY4Qy5ZN9kMUpsMFIbD9zPXH/edit"

def download_file_from_google_drive(url, destination):
    session = requests.Session()

    response = session.get(url, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'confirm' : token }
        response = session.get(url, params = params, stream = True)

    save_response_content(response, destination)   

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def extract_file_id_from_google_drive_url(url):
    pattern = r'/d/([0-9A-Za-z_-]{33}|[0-9A-Za-z_-]{19})'
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None
    
def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

# # Create a folder named "photo" if it doesn't exist
# folder_path = r'./client/public/temp'  # Use a raw string
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)

# # Extracting file ID from the Google Drive URL
# file_id = extract_file_id_from_google_drive_url(url)
# # Creating a direct download URL for the Google Drive file
# file_url = f'https://drive.google.com/uc?id={file_id}&export=download'

# # The path where you want to save the downloaded file, inside the "photo" folder
# destination = os.path.join(folder_path, 'downloaded.glb')

# download_file_from_google_drive(file_url, destination)