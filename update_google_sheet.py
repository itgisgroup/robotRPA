import gspread
from google.oauth2.service_account import Credentials
import datetime

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def update_google_sheet(sheet_id, file_name, drawing_id):
    """Cập nhật Google Sheet và di chuyển dòng sang sheet hoàn thành"""
    try:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Lấy các worksheet
        main_sheet = client.open_by_key(sheet_id).worksheet("Danh sách file cần upload")
        completed_sheet = client.open_by_key(sheet_id).worksheet("Upload Hoàn thành")
        
        # Lấy tất cả dữ liệu từ sheet chính
        data = main_sheet.get_all_records()
        
        # Tìm dòng cần cập nhật
        for idx, row in enumerate(data, start=2):  # start=2 vì dòng 1 là header
            if row["Tên file (File name)"] == file_name:
                # Cập nhật ID file CADDi và trạng thái
                main_sheet.update_cell(idx, 7, drawing_id)  # Cột ID file CADDi
                main_sheet.update_cell(idx, 8, "Hoàn thành")  # Cột Trạng thái
                
                # Chuẩn bị dữ liệu để chuyển sang sheet hoàn thành
                completed_data = [
                    row["STT"],
                    row["Tên dự án (Project)"],
                    row["Đường dẫn file"],
                    row["Tên file (File name)"],
                    row["Mô tả (Description)"],
                    drawing_id,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
                
                # Thêm dòng vào sheet hoàn thành
                completed_sheet.append_row(completed_data)
                
                # Xóa dòng khỏi sheet chính
                main_sheet.delete_rows(idx)
                
                print(f"Đã cập nhật và di chuyển file {file_name} sang sheet hoàn thành")
                return True
                
        print(f"Không tìm thấy file {file_name} trong sheet")
        return False
        
    except Exception as e:
        print(f"Lỗi khi cập nhật Google Sheet: {str(e)}")
        return False
