from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import time

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_drive_service():
    """Initialize Google Drive service"""
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def download_file(file_id, destination_path):
    """Download file from Google Drive"""
    service = get_drive_service()
    
    try:
        print(f"Starting download of file {file_id}")
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        
        # Tăng thời gian timeout và thêm retry
        max_retries = 3
        retry_count = 0
        timeout = 300  # 5 phút
        
        start_time = time.time()
        while done is False:
            try:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download progress: {int(status.progress() * 100)}%")
                
                # Kiểm tra timeout
                if time.time() - start_time > timeout:
                    raise TimeoutError("Download timeout")
                    
            except Exception as e:
                if retry_count < max_retries:
                    print(f"Error during download, retrying... ({retry_count + 1}/{max_retries})")
                    retry_count += 1
                    time.sleep(5)  # Đợi 5 giây trước khi thử lại
                    continue
                else:
                    raise e
        
        # Save the file
        print(f"Saving file to {destination_path}")
        with open(destination_path, 'wb') as f:
            f.write(file.getvalue())
        print("Download completed successfully")
        return True
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def move_file_to_completed(file_id, completed_folder_id):
    """Move file to completed folder"""
    service = get_drive_service()
    
    try:
        # Get the file's current parents
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        
        # Move the file to the new folder
        file = service.files().update(
            fileId=file_id,
            addParents=completed_folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        
        return True
    except Exception as e:
        print(f"Error moving file: {str(e)}")
        return False

def get_file_id_from_path(file_path):
    """Extract file ID from Google Drive path"""
    # Remove 'https://drive.google.com/file/d/' and '/view' from the path
    file_id = file_path.split('/d/')[1].split('/')[0]
    return file_id 