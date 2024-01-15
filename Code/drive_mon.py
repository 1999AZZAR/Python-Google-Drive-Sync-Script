import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time
import io
import sqlite3
from datetime import datetime

# Get the absolute path of the current script
script_path = os.path.dirname(os.path.abspath(__file__))

# Read API key, credentials path, folder ID, and download path from the .secret file
secret_file_path = os.path.join(script_path, '.secret')
with open(secret_file_path, 'r') as secret_file:
    secret_data = secret_file.read()
    exec(secret_data)

# Build the Google Drive API service
service = build('drive', 'v3', developerKey=API_KEY)

# Connect to SQLite database
db_path = os.path.join(DOWNLOAD_PATH, 'file_log.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for file log if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        download_timestamp TEXT,
        file_size INTEGER
    )
''')
conn.commit()

def list_files(service, folder_id):
    result = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, size)").execute()
    files = result.get('files', [])
    return files

def download_file(service, file_id, file_name, download_path):
    file_path = os.path.join(download_path, file_name)
    request = service.files().get_media(fileId=file_id)
    downloader = io.FileIO(file_path, 'wb')
    downloader.write(request.execute())

    # Get file size
    file_info = service.files().get(fileId=file_id, fields="size").execute()
    file_size = file_info.get('size', 0)

    # Log file download information to the database
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO file_log (name, download_timestamp, file_size) VALUES (?, ?, ?)', (file_name, timestamp, file_size))
    conn.commit()

def remove_file(file_name, download_path):
    file_path = os.path.join(download_path, file_name)

    # Remove file from the downloaded folder
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove file entry from the database
    cursor.execute('DELETE FROM file_log WHERE name = ?', (file_name,))
    conn.commit()

# Check the database for already downloaded files
cursor.execute('SELECT name FROM file_log')
downloaded_files = set(row[0] for row in cursor.fetchall())

# Initial file list
files = list_files(service, FOLDER_ID)

# Download and cleanup existing files
for file in files:
    if file['name'] not in downloaded_files:
        print(f"Downloading existing file: {file['name']}...")
        download_file(service, file['id'], file['name'], DOWNLOAD_PATH)

# Monitor for changes every 15 seconds
while True:
    time.sleep(15)

    # Get the updated file list
    updated_files = list_files(service, FOLDER_ID)

    # Find new files
    new_files = [file for file in updated_files if file not in files]

    # Download new files
    for file in new_files:
        if file['name'] not in downloaded_files:
            print(f"Downloading new file: {file['name']}...")
            download_file(service, file['id'], file['name'], DOWNLOAD_PATH)

    # Find deleted files
    deleted_files = [file for file in files if file not in updated_files]

    # Remove deleted files
    for file in deleted_files:
        print(f"File deleted: {file['name']}")
        remove_file(file['name'], DOWNLOAD_PATH)

    # Update the file list
    files = updated_files
