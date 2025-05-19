import os
import glob
import time
from bot_caddi import upload_to_caddi
from excel_handler import ExcelHandler
from logger import BotLogger
import shutil
from datetime import datetime

# Cấu hình đường dẫn
FILE_CHO_XU_LY_DIR = "/Users/hlethanh486/Desktop/robotTH/File-ChoXuLy"
FILE_HOAN_THANH_DIR = "/Users/hlethanh486/Desktop/robotTH/File-Hoanthanh"
TMF_SOURCE_DIR = "/Users/hlethanh486/Desktop/robotTH/TMF-nguon"
TMF_UPLOAD_DIR = "/Users/hlethanh486/Desktop/robotTH/TMF-upload"
USERNAME = "uyennguyen@inthuanhung.com.vn"
PASSWORD = "@thla123456"
CADDI_URL = "https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460"

def ensure_directories():
    for dir_path in [TMF_SOURCE_DIR, TMF_UPLOAD_DIR, FILE_HOAN_THANH_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Đã tạo thư mục: {dir_path}")

def move_file_to_upload(source_path):
    filename = os.path.basename(source_path)
    dest_path = os.path.join(TMF_UPLOAD_DIR, filename)
    shutil.move(source_path, dest_path)
    return dest_path

def upload_all_files(excel_handler, logger, page):
    import time
    start_time = time.time()
    pending_files = excel_handler.read_pending_files()
    print(f"\n=== Bắt đầu upload {len(pending_files)} file ===")
    # Đếm số file thực tế trong TMF-nguon
    file_names_in_excel = [file['Tên file (File name)'] for file in pending_files]
    files_in_source = set(os.listdir(TMF_SOURCE_DIR))
    missing_files = [f for f in file_names_in_excel if f not in files_in_source]
    print(f"Số file cần upload (theo Excel): {len(file_names_in_excel)}")
    print(f"Số file thực tế có trong TMF-nguon: {len(files_in_source)}")
    if missing_files:
        print("Cảnh báo: Có file trong Excel không tìm thấy trong TMF-nguon:")
        for f in missing_files:
            print(f"  - {f}")
    success_count = 0
    fail_count = 0
    is_first_upload = True
    for file in pending_files:
        file_name = file['Tên file (File name)']
        project_name = file['Tên dự án (Project)']
        file_category = file['File category']
        description = file['Mô tả (Description)']
        file_path = os.path.join(TMF_SOURCE_DIR, file_name)
        try:
            excel_handler.update_status(file_name, "Đang xử lý")
            logger.log(f"Bắt đầu xử lý file {file_name}")
            result = upload_to_caddi(
                USERNAME, PASSWORD,
                project_name,
                file_path,
                description,
                file_category,
                page,
                is_first_upload=is_first_upload
            )
            is_first_upload = False
            if result:
                print(f"Upload thành công file {file_name}")
                excel_handler.update_status(file_name, "Upload thành công")
                logger.log_success(f"Upload thành công file {file_name}")
                move_file_to_upload(file_path)
                excel_handler.move_to_completed(file_name)
                success_count += 1
            else:
                print(f"Upload thất bại file {file_name}")
                excel_handler.update_status(file_name, "Lỗi upload")
                logger.log_error(f"Upload thất bại file {file_name}")
                fail_count += 1
        except Exception as e:
            error_msg = f"Lỗi xử lý file {file_name}: {str(e)}"
            excel_handler.update_status(file_name, f"Lỗi upload: {str(e)}")
            print(error_msg)
            logger.log_error(error_msg)
            fail_count += 1
    end_time = time.time()
    total_time = end_time - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    print(f"\n=== Kết thúc upload ===")
    print(f"Tổng số file upload thành công: {success_count}")
    print(f"Tổng số file upload thất bại: {fail_count}")
    print(f"Tổng thời gian thực hiện: {hours} giờ {minutes} phút {seconds} giây")

def main():
    ensure_directories()
    # Lấy danh sách file Excel Upload_FileDrawer_*.xlsx
    excel_files = glob.glob(os.path.join(FILE_CHO_XU_LY_DIR, 'Upload_FileDrawer_*.xlsx'))
    if not excel_files:
        print(f"\nKhông có file Excel nào dạng Upload_FileDrawer_*.xlsx trong {FILE_CHO_XU_LY_DIR} để xử lý.")
        return
    for excel_path in excel_files:
        logger = BotLogger(excel_path, "bot_upload.log")
        print(f"\n==============================\nBẮT ĐẦU XỬ LÝ FILE: {os.path.basename(excel_path)}\n==============================")
        excel_handler = ExcelHandler(excel_path)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto(CADDI_URL)
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
            upload_all_files(excel_handler, logger, page)
            browser.close()
        # Sau khi upload xong, di chuyển file Excel sang File-Hoanthanh
        now = datetime.now().strftime('%d%m%Y_%H%M%S')
        file_name = os.path.basename(excel_path)
        new_file_name = f"hoanthanh_{now}_{file_name}"
        dest_path = os.path.join(FILE_HOAN_THANH_DIR, new_file_name)
        try:
            shutil.move(excel_path, dest_path)
            print(f"Đã di chuyển file Excel hoàn thành sang: {dest_path}")
        except Exception as e:
            print(f"Lỗi khi di chuyển file Excel: {str(e)}")

if __name__ == "__main__":
    main() 