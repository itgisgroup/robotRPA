import os
import tempfile
import datetime
import time
from playwright.sync_api import sync_playwright
from google_auth import get_google_sheet
from bot_caddi import upload_to_caddi
from update_google_sheet import update_google_sheet
from google_drive import download_file, move_file_to_completed, get_file_id_from_path
from logger import BotLogger

# Configuration
SHEET_ID = "1FsYA4nfB0eHIWMJC7oNEo7a9zvcXE6qYlyTgF_ntFXs"
COMPLETED_FOLDER_ID = "1yeogE9ZA3ePvPcJM8x3EX9AOs-X1q5a4"
USERNAME = "uyennguyen@inthuanhung.com.vn"
PASSWORD = "@thla123456"

def process_files():
    # Initialize logger
    logger = BotLogger(SHEET_ID, "Logs")
    
    try:
        # 1. Đọc danh sách file từ Google Sheet
        logger.log("Bắt đầu quá trình xử lý file...")
        sheet = get_google_sheet(SHEET_ID, "Danh sách file cần upload")
        data = sheet.get_all_records()
        
        logger.log(f"Tìm thấy {len(data)} file cần xử lý")
        
        # Khởi tạo trình duyệt một lần cho tất cả các file
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                slow_mo=100
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            page.set_default_timeout(120000)
            
            # Truy cập trang CADDi và đăng nhập
            page.goto("https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460")
            time.sleep(10)
            
            # Đăng nhập
            username_input = page.locator('input[type="text"]').first
            if username_input:
                username_input.fill(USERNAME)
                time.sleep(2)
            
            password_input = page.locator('input[type="password"]').first
            if password_input:
                password_input.fill(PASSWORD)
                time.sleep(2)
            
            submit_button = page.locator('button[type="submit"]').first
            if submit_button:
                submit_button.click()
                time.sleep(15)
            
            # Xử lý từng file
            for row in data:
                if row["Trạng thái"] == "Chờ xử lý":
                    file_name = row["Tên file (File name)"]
                    try:
                        project_name = row["Tên dự án (Project)"]
                        description = row["Mô tả (Description)"]
                        file_path = row["Đường dẫn file"]
                        
                        logger.log(f"Đang xử lý file: {file_name}")
                        
                        # 2. Tải file từ Google Drive
                        with tempfile.TemporaryDirectory() as temp_dir:
                            logger.log(f"Đang tải file từ Google Drive...")
                            file_id = get_file_id_from_path(file_path)
                            local_file_path = os.path.join(temp_dir, file_name)
                            
                            if not download_file(file_id, local_file_path):
                                logger.log_error(f"Không thể tải file: {file_name}")
                                continue
                            
                            # 3 & 4. Upload file lên CADDi Drawer và cập nhật mô tả
                            logger.log(f"Đang upload file lên CADDi Drawer...")
                            drawing_id = upload_to_caddi(USERNAME, PASSWORD, project_name, local_file_path, description, page)
                            
                            if drawing_id:
                                # 5 & 6. Cập nhật Google Sheet với Drawing ID và di chuyển dòng sang sheet hoàn thành
                                logger.log(f"Đang cập nhật Google Sheet với Drawing ID: {drawing_id}")
                                if update_google_sheet(SHEET_ID, file_name, drawing_id):
                                    logger.log_success(f"Đã cập nhật Google Sheet và di chuyển dòng sang sheet hoàn thành: {file_name}")
                                    
                                    # 7. Di chuyển file sang thư mục hoàn thành
                                    logger.log(f"Đang di chuyển file sang thư mục hoàn thành...")
                                    if move_file_to_completed(file_id, COMPLETED_FOLDER_ID):
                                        logger.log_success(f"Đã di chuyển file sang thư mục hoàn thành: {file_name}")
                                    else:
                                        logger.log_error(f"Không thể di chuyển file sang thư mục hoàn thành: {file_name}")
                                else:
                                    logger.log_error(f"Không thể cập nhật Google Sheet: {file_name}")
                            else:
                                logger.log_error(f"Không thể upload file lên CADDi: {file_name}")
                        
                        # Quay lại trang chủ sau khi xử lý xong mỗi file
                        logger.log("Quay lại trang chủ...")
                        page.goto("https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460")
                        time.sleep(10)
                    
                    except Exception as e:
                        logger.log_error(f"Lỗi khi xử lý file {file_name}: {str(e)}")
                        # Quay lại trang chủ nếu có lỗi
                        try:
                            page.goto("https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460")
                            time.sleep(10)
                        except:
                            pass
                        continue
            
            # Đóng trình duyệt sau khi xử lý xong tất cả các file
            context.close()
            browser.close()
            logger.log("Đã đóng trình duyệt")
        
        logger.log("Hoàn thành quá trình xử lý file")
        
    except Exception as e:
        logger.log_error(f"Lỗi nghiêm trọng: {str(e)}")
    
    finally:
        # Lưu log vào Google Sheet
        try:
            sheet = get_google_sheet(SHEET_ID, "Logs")
            logs = logger.get_logs().split("\n")
            for log in logs:
                if log.strip():  # Chỉ thêm log không rỗng
                    sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log])
        except Exception as e:
            print(f"Lỗi khi lưu log: {str(e)}")

if __name__ == "__main__":
    process_files()
