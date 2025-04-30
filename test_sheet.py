import gspread
from google.oauth2.service_account import Credentials

def test_connection():
    print("Testing connection to Google Sheet...")
    
    # Sheet ID từ URL của bạn
    SHEET_ID = "1FsYA4nfB0eHIWMJC7oNEo7a9zvcXE6qYlyTgF_ntFXs"
    print(f"Sheet ID: {SHEET_ID}")
    
    try:
        # Khởi tạo credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        
        print("Attempting to get sheet 'Danh sách file cần upload'...")
        sheet = client.open_by_key(SHEET_ID).worksheet("Danh sách file cần upload")
        
        # Thử đọc dữ liệu
        data = sheet.get_all_records()
        print(f"Successfully connected! Found {len(data)} rows of data.")
        
        # In ra 2 dòng đầu tiên để kiểm tra
        if len(data) > 0:
            print("\nFirst row data:")
            print(data[0])
        
    except Exception as e:
        print("Error details:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Error args: {e.args}")

if __name__ == "__main__":
    test_connection() 