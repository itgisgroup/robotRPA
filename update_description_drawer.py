import os
import glob
import time
from bot_caddi import find_file_and_get_drawing_id, update_description
from excel_handler import ExcelHandler
from logger import BotLogger
import shutil
from datetime import datetime

FILE_CHO_XU_LY_DIR = "/Users/hlethanh486/Desktop/robotTH/File-ChoXuLy"
FILE_HOAN_THANH_DIR = "/Users/hlethanh486/Desktop/robotTH/File-Hoanthanh"
USERNAME = "uyennguyen@inthuanhung.com.vn"
PASSWORD = "@thla123456"
CADDI_URL = "https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460"

def update_ds_drawingid_on_software(page, drawing_id):
    """Cập nhật trường Ds DrawingID trên phần mềm"""
    try:
        # 1. Click vào nút Edit (bút chì) cạnh Ds DrawingID
        edit_btn = page.locator('button:has(svg[data-testid="EditOutlinedIcon"])').first
        if edit_btn and edit_btn.is_visible():
            edit_btn.click()
            time.sleep(2)
        else:
            print("Không tìm thấy nút Edit Ds DrawingID")
            return False

        # 2. Tìm trường input để nhập DrawingID
        ds_input = page.locator('input[name="Ds DrawingID[0].value"]').first
        if ds_input and ds_input.is_visible():
            ds_input.fill(drawing_id)
            time.sleep(1)
            # 3. Click nút Save
            save_btn = page.locator('button[type="submit"]:has-text("Save")').first
            if save_btn and save_btn.is_visible():
                save_btn.click()
                time.sleep(2)
                print("Đã cập nhật Ds DrawingID trên phần mềm")
                return True
            else:
                print("Không tìm thấy nút Save cho Ds DrawingID")
                return False
        else:
            print("Không tìm thấy trường nhập Ds DrawingID")
            return False
    except Exception as e:
        print(f"Lỗi khi cập nhật Ds DrawingID: {str(e)}")
        return False

def process_update(excel_handler, logger, page):
    start_time = time.time()
    # Đọc các dòng có trạng thái Chờ xử lý
    files = excel_handler.read_files_to_update()
    print(f"\n=== Bắt đầu cập nhật {len(files)} file ===")
    total_files = len(files)
    success_count = 0
    fail_count = 0
    for file in files:
        file_name = file['Tên file (File name)']
        description = file['Mô tả (Description)']
        try:
            logger.log(f"Bắt đầu cập nhật file {file_name}")
            # Quay về trang chủ
            page.goto(CADDI_URL)
            time.sleep(10)
            # Tìm file và lấy DrawingID
            drawing_id = find_file_and_get_drawing_id(page, file_name)
            if drawing_id:
                # Cập nhật Description
                if update_description(page, description):
                    # Ghi DrawingID vào cột ID file (CADDi) trong Excel
                    excel_handler.update_drawing_id(file_name, drawing_id)
                    # Cập nhật Ds DrawingID trên phần mềm
                    if update_ds_drawingid_on_software(page, drawing_id):
                        excel_handler.update_status(file_name, "Hoàn thành")
                        excel_handler.move_to_completed(file_name)  # Di chuyển dòng sang sheet hoàn thành
                        logger.log_success(f"Đã hoàn thành cập nhật file {file_name}")
                        success_count += 1
                    else:
                        excel_handler.update_status(file_name, "Lỗi cập nhật Ds DrawingID")
                        logger.log_error(f"Lỗi cập nhật Ds DrawingID cho file {file_name}")
                        fail_count += 1
                else:
                    excel_handler.update_status(file_name, "Lỗi cập nhật Description")
                    logger.log_error(f"Lỗi cập nhật Description cho file {file_name}")
                    fail_count += 1
            else:
                excel_handler.update_status(file_name, "Lỗi lấy DrawingID")
                logger.log_error(f"Không tìm thấy DrawingID cho file {file_name}")
                fail_count += 1
        except Exception as e:
            excel_handler.update_status(file_name, f"Lỗi cập nhật: {str(e)}")
            logger.log_error(f"Lỗi cập nhật file {file_name}: {str(e)}")
            fail_count += 1
    end_time = time.time()
    total_time = end_time - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    print(f"\n=== Kết thúc cập nhật ===")
    print(f"Tổng số file cần xử lý: {total_files}")
    print(f"Tổng số file hoàn thành: {success_count}")
    print(f"Tổng số file lỗi: {fail_count}")
    print(f"Tổng thời gian thực hiện: {hours} giờ {minutes} phút {seconds} giây")

def main():
    # Lấy danh sách file Excel Update_DescriptionDrawer_*.xlsx
    excel_files = glob.glob(os.path.join(FILE_CHO_XU_LY_DIR, 'Update_DescriptionDrawer_*.xlsx'))
    if not excel_files:
        print(f"\nKhông có file Excel nào dạng Update_DescriptionDrawer_*.xlsx trong {FILE_CHO_XU_LY_DIR} để xử lý.")
        return
    for excel_path in excel_files:
        logger = BotLogger(excel_path, "bot_update.log")
        print(f"\n==============================\nBẮT ĐẦU XỬ LÝ FILE: {os.path.basename(excel_path)}\n==============================")
        excel_handler = ExcelHandler(excel_path, main_sheet="Danh sách file cần update", completed_sheet="Update Hoàn thành")
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
            process_update(excel_handler, logger, page)
            browser.close()
        # Sau khi xử lý xong, di chuyển file Excel sang File-Hoanthanh
        now = datetime.now().strftime('%d%m%Y_%H%M%S')
        file_name = os.path.basename(excel_path)
        new_file_name = f"hoanthanh_{now}_{file_name}"
        dest_path = os.path.join(FILE_HOAN_THANH_DIR, new_file_name)
        try:
            shutil.move(excel_path, dest_path)
            print(f"Đã di chuyển file hoàn thành sang: {dest_path}")
        except Exception as e:
            print(f"Lỗi khi di chuyển file Excel: {str(e)}")

if __name__ == "__main__":
    main() 