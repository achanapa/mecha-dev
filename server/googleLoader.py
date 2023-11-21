import requests
import os
from pymongo import MongoClient
import re

def download_from_google_drive(url, destination):
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