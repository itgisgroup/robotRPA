import os
import time
from playwright.sync_api import sync_playwright
from bot_caddi import upload_to_caddi, find_file_and_get_drawing_id, update_description
from excel_handler import ExcelHandler
from logger import BotLogger
import shutil

# Configuration
EXCEL_PATH = "/Users/hlethanh486/Desktop/robotTH/Update_DescriptionDrawer.xlsx"
TMF_SOURCE_DIR = "/Users/hlethanh486/Desktop/robotTH/TMF-nguon"
TMF_UPLOAD_DIR = "/Users/hlethanh486/Desktop/robotTH/TMF-upload"
TMF_COMPLETED_DIR = "/Users/hlethanh486/Desktop/robotTH/TMF-completed"
USERNAME = "uyennguyen@inthuanhung.com.vn"
PASSWORD = "@thla123456"
CADDI_URL = "https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460"

def ensure_directories():
    """Đảm bảo các thư mục cần thiết tồn tại"""
    for dir_path in [TMF_SOURCE_DIR, TMF_UPLOAD_DIR, TMF_COMPLETED_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Đã tạo thư mục: {dir_path}")

def move_file_to_upload(source_path):
    """Di chuyển file từ TMF-nguon sang TMF-upload"""
    filename = os.path.basename(source_path)
    dest_path = os.path.join(TMF_UPLOAD_DIR, filename)
    shutil.copy2(source_path, dest_path)
    return dest_path

def move_file_to_completed(upload_path):
    """Di chuyển file từ TMF-upload sang TMF-completed"""
    filename = os.path.basename(upload_path)
    dest_path = os.path.join(TMF_COMPLETED_DIR, filename)
    shutil.move(upload_path, dest_path)
    return dest_path

def upload_all_files(excel_handler, logger, page):
    """Upload tất cả file chờ xử lý"""
    pending_files = excel_handler.read_pending_files()
    print(f"\n=== Bắt đầu upload {len(pending_files)} file ===")
    
    for file in pending_files:
        file_name = None  # Initialize file_name outside try block
        try:
            file_name = file['Tên file (File name)']
            project_name = file['Tên dự án (Project)']
            file_category = file['File category']
            description = file['Mô tả (Description)']
            file_path = os.path.join(TMF_SOURCE_DIR, file_name)
            
            print(f"\nĐang xử lý file: {file_name}")
            
            # Cập nhật trạng thái đang xử lý
            excel_handler.update_status(file_name, "Đang xử lý")
            logger.log(f"Bắt đầu xử lý file {file_name}")
            
            # Upload file
            result = upload_to_caddi(
                USERNAME, PASSWORD,
                project_name,
                file_path,
                description,
                file_category,
                page
            )
            
            if result:
                # Upload thành công
                print(f"Upload thành công file {file_name}")
                excel_handler.update_status(file_name, "Đã upload thành công")
                logger.log_success(f"Upload thành công file {file_name}")
                
                # Di chuyển file sang thư mục upload
                excel_handler.move_file(file_name, TMF_SOURCE_DIR, TMF_UPLOAD_DIR)
            else:
                # Upload thất bại
                print(f"Upload thất bại file {file_name}")
                excel_handler.update_status(file_name, "Chờ xử lý")
                logger.log_error(f"Upload thất bại file {file_name}")
                
        except Exception as e:
            error_msg = f"Lỗi xử lý file: {str(e)}"
            if file_name:
                error_msg = f"Lỗi xử lý file {file_name}: {str(e)}"
                excel_handler.update_status(file_name, "Chờ xử lý")
            print(error_msg)
            logger.log_error(error_msg)

def process_uploaded_files(excel_handler, logger, page):
    """Xử lý các file đã upload thành công"""
    uploaded_files = excel_handler.read_uploaded_files()
    print(f"\n=== Bắt đầu xử lý {len(uploaded_files)} file đã upload ===")
    
    for file in uploaded_files:
        try:
            file_name = file['Tên file (File name)']
            description = file['Mô tả (Description)']
            
            print(f"\nĐang xử lý file đã upload: {file_name}")
            logger.log(f"Bắt đầu xử lý file đã upload {file_name}")
            
            # Quay về trang chủ
            page.goto(CADDI_URL)
            time.sleep(10)
            
            # Tìm file và lấy Drawing ID
            drawing_id = find_file_and_get_drawing_id(page, file_name)
            
            if drawing_id:
                # Cập nhật Description
                if update_description(page, description):
                    # Cập nhật Drawing ID vào Excel
                    excel_handler.update_drawing_id(file_name, drawing_id)
                    logger.log_success(f"Đã cập nhật Drawing ID {drawing_id} cho file {file_name}")
                    
                    # Cập nhật trạng thái thành Hoàn thành
                    excel_handler.update_status(file_name, "Hoàn thành")
                    
                    # Di chuyển file sang completed
                    excel_handler.move_file(file_name, TMF_UPLOAD_DIR, TMF_COMPLETED_DIR)
                    
                    # Di chuyển dòng sang sheet hoàn thành
                    excel_handler.move_to_completed(file_name)
                    
                    logger.log_success(f"Đã hoàn thành xử lý file {file_name}")
                else:
                    print(f"Không thể cập nhật Description cho file {file_name}")
                    excel_handler.update_status(file_name, "Lỗi")
                    logger.log_error(f"Lỗi cập nhật Description cho file {file_name}")
            else:
                print(f"Không tìm thấy Drawing ID cho file {file_name}")
                excel_handler.update_status(file_name, "Lỗi")
                logger.log_error(f"Không tìm thấy Drawing ID cho file {file_name}")
                
        except Exception as e:
            print(f"Lỗi xử lý file đã upload {file_name}: {str(e)}")
            excel_handler.update_status(file_name, "Lỗi")
            logger.log_error(f"Lỗi xử lý file đã upload {file_name}: {str(e)}")

def main():
    """Hàm chính thực hiện toàn bộ quy trình"""
    # Bắt đầu đếm thời gian
    start_time = time.time()
    
    # Khởi tạo các thành phần
    excel_handler = ExcelHandler(EXCEL_PATH)
    logger = BotLogger(EXCEL_PATH, "bot.log")
    
    try:
        # Đảm bảo các thư mục tồn tại
        ensure_directories()
        
        # Kiểm tra các file cần xử lý trước
        pending_files = excel_handler.read_pending_files()
        if not pending_files:
            print("\nKhông có file nào cần xử lý. Vui lòng kiểm tra lại trạng thái trong file Excel.")
            return
            
        print(f"\nĐã tìm thấy {len(pending_files)} file cần xử lý.")
        
        with sync_playwright() as p:
            # Khởi tạo browser
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            
            # Truy cập trang và đăng nhập
            print("\n=== ĐĂNG NHẬP ===")
            page.goto(CADDI_URL)
            time.sleep(10)  # Khôi phục lại 10s cho trang load
            
            # Đăng nhập
            print("Đang đăng nhập...")
            username_input = page.locator('input[type="text"]').first
            if username_input:
                username_input.fill(USERNAME)
                time.sleep(2)  # Khôi phục lại 2s
            
            password_input = page.locator('input[type="password"]').first
            if password_input:
                password_input.fill(PASSWORD)
                time.sleep(2)  # Khôi phục lại 2s
            
            submit_button = page.locator('button[type="submit"]').first
            if submit_button:
                submit_button.click()
                time.sleep(15)  # Khôi phục lại 15s cho đăng nhập
            
            # BƯỚC 1: Upload tất cả file
            print("\n=== BƯỚC 1: UPLOAD TẤT CẢ FILE ===")
            upload_all_files(excel_handler, logger, page)
            
            # BƯỚC 2: Xử lý các file đã upload thành công
            print("\n=== BƯỚC 2: XỬ LÝ CÁC FILE ĐÃ UPLOAD ===")
            process_uploaded_files(excel_handler, logger, page)
            
            # Đóng browser
            browser.close()
            
    except Exception as e:
        logger.log_error(f"Lỗi chương trình: {str(e)}")
        print(f"Lỗi chương trình: {str(e)}")
    
    finally:
        # Tính và hiển thị tổng thời gian thực hiện
        end_time = time.time()
        total_time = end_time - start_time
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        
        time_msg = f"\nTổng thời gian thực hiện: {hours} giờ {minutes} phút {seconds} giây"
        print(time_msg)
        logger.log(time_msg)

if __name__ == "__main__":
    main() 