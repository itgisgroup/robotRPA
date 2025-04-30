# CADDi Drawer File Upload Automation

This project automates the process of uploading PDF files from Google Drive to CADDi Drawer, with automatic status tracking and logging.

## Features

- Automated file upload from Google Drive to CADDi Drawer
- Google Sheets integration for file tracking
- Automatic status updates and logging
- File movement to completed folder after successful upload
- Error handling and logging

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with enabled APIs:
  - Google Drive API
  - Google Sheets API
- CADDi Drawer account
- Service account credentials (credentials.json)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Configure the following in `main.py`:
- `SHEET_ID`: Your Google Sheet ID
- `COMPLETED_FOLDER_ID`: ID of the Google Drive folder for completed files
- `USERNAME`: Your CADDi Drawer email
- `PASSWORD`: Your CADDi Drawer password

4. Ensure your Google Sheet has the following columns:
- Tên dự án (Project Name)
- Tên file (File Name)
- Mô tả (Description)
- Đường dẫn file (File Path)
- ID file CADDi (CADDi File ID)
- Trạng thái (Status)

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Read files from the Google Sheet
2. Download files from Google Drive
3. Upload them to CADDi Drawer
4. Update the sheet with results
5. Move completed files to the completed folder
6. Log all activities

## Logging

Logs are stored in:
- `bot.log` file
- "Logs" sheet in the Google Sheet

## Error Handling

The script includes comprehensive error handling:
- Individual file processing errors
- Network errors
- API errors
- Authentication errors

All errors are logged and tracked in the Google Sheet. 