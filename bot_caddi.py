from playwright.sync_api import sync_playwright, TimeoutError
import time
import os
import math

CADDI_URL = "https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460"

# Biến lưu trữ Project và Category hiện tại
current_project = None
current_category = None

def wait_for_modal_close(page):
    """Đợi modal backdrop biến mất"""
    try:
        # Đợi cho đến khi không còn modal backdrop
        page.wait_for_selector('div.MuiBackdrop-root', state='hidden', timeout=5000)
        time.sleep(1)  # Đợi thêm 1s để đảm bảo modal đã đóng hoàn toàn
        return True
    except:
        return False

def upload_to_caddi(username, password, project_name, file_path, description, file_category, page=None, is_first_upload=False):
    global current_project, current_category
    
    # Chuẩn hóa file_category
    if file_category is None or (isinstance(file_category, float) and math.isnan(file_category)) or str(file_category).strip().lower() in ["", "nan", "none"]:
        file_category = None
    
    print(f"\nTên dự án từ Google Sheet: {project_name}")
    print(f"File category: {file_category}")
    print(f"Đường dẫn file cần upload: {file_path}")
    print(f"Tên file: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
        return None
        
    print(f"Kích thước file: {os.path.getsize(file_path)} bytes")
    
    try:
        # Kiểm tra xem có cần chọn lại Project và Category không
        need_select_project = current_project != project_name
        need_select_category = current_category != file_category
        
        # Nếu là lần đầu upload, phải click nút Upload để mở form
        if is_first_upload:
            print("Lần đầu upload, cần mở form upload")
            print("Đang tìm nút Upload ở góc phải...")
            upload_button = page.locator('button.MuiButton-contained:has-text("Upload")').first
            if upload_button:
                print("Đã tìm thấy nút Upload")
                upload_button.click()
                print("Đã click nút Upload")
                time.sleep(5)  # Đợi form hiện lên đầy đủ
            else:
                print("Không tìm thấy nút Upload")
                return None
        
        # Chọn lại Project nếu cần
        if is_first_upload or need_select_project:
            print(f"Cần chọn Project (hiện tại: {current_project}, mới: {project_name})")
            # Tìm ô Project
            print("Đang tìm ô Project...")
            project_input = page.locator('label:has-text("Project") + div input').first
            if project_input:
                print("Đã tìm thấy ô Project")
                project_input.click()
                time.sleep(2)
                
                # Nhập tên dự án
                print(f"Đang nhập tên dự án: {project_name}")
                project_input.fill(project_name)
                print("Đã nhập tên dự án")
                time.sleep(3)
                
                # Chọn dự án trong kết quả tìm kiếm
                print("Đang tìm dự án trong kết quả tìm kiếm...")
                project_option = page.locator(f'div[role="presentation"] li[role="option"]:text-is("{project_name}")').first
                if project_option:
                    print("Đã tìm thấy dự án, đang click...")
                    project_option.click()
                    print("Đã click chọn dự án")
                    time.sleep(2)
                    current_project = project_name
                else:
                    print("Không tìm thấy dự án trong kết quả tìm kiếm")
                    return None
            else:
                print("Không tìm thấy ô Project")
                return None

        # Xử lý chọn File Category
        if is_first_upload:
            if file_category:
                print("Lần đầu upload và có File Category, tiến hành chọn category.")
                # Tìm ô File Category
                category_input = page.locator('label:has-text("File category") + div input').first
                if category_input:
                    print("Đã tìm thấy ô File Category")
                    category_input.click()
                    time.sleep(2)
                    print(f"Đang nhập File Category: {file_category}")
                    category_input.fill(file_category)
                    print("Đã nhập File Category")
                    time.sleep(3)
                    print("Đang tìm category trong dropdown...")
                    category_option = page.locator(f'div[role="presentation"] li[role="option"]:text-is("{file_category}")').first
                    if category_option:
                        print("Đã tìm thấy category, đang click...")
                        category_option.click()
                        print("Đã click chọn category")
                        time.sleep(2)
                        current_category = file_category
                    else:
                        print("Không tìm thấy category trong dropdown")
                        return None
                else:
                    print("Không tìm thấy ô File Category")
                    return None
            else:
                print("Lần đầu upload và không có File Category, bỏ qua bước chọn category.")
                current_category = None
        else:
            if file_category:
                if current_category and file_category != current_category:
                    # Đã có category trước đó và khác category mới, cần clear trước khi chọn lại
                    category_input = page.locator('label:has-text("File category") + div input').first
                    if category_input:
                        clear_btn = page.locator('label:has-text("File category") + div button[aria-label="Clear"]').first
                        if clear_btn and clear_btn.is_visible():
                            print("Đang clear trường File Category cũ...")
                            clear_btn.click()
                            time.sleep(1)
                        else:
                            print("Không tìm thấy hoặc không hiển thị nút clear File Category.")
                if not current_category or (current_category and file_category != current_category):
                    # Sau khi clear (nếu cần), chọn category mới
                    print(f"Cần chọn File Category (hiện tại: {current_category}, mới: {file_category})")
                    category_input = page.locator('label:has-text("File category") + div input').first
                    if category_input:
                        print("Đã tìm thấy ô File Category")
                        category_input.click()
                        time.sleep(2)
                        print(f"Đang nhập File Category: {file_category}")
                        category_input.fill(file_category)
                        print("Đã nhập File Category")
                        time.sleep(3)
                        print("Đang tìm category trong dropdown...")
                        category_option = page.locator(f'div[role="presentation"] li[role="option"]:text-is("{file_category}")').first
                        if category_option:
                            print("Đã tìm thấy category, đang click...")
                            category_option.click()
                            print("Đã click chọn category")
                            time.sleep(2)
                            current_category = file_category
                        else:
                            print("Không tìm thấy category trong dropdown")
                            return None
                    else:
                        print("Không tìm thấy ô File Category")
                        return None
                else:
                    print("Giữ nguyên category, không cần thao tác lại.")
            else:
                print("Không có File Category, bỏ qua bước chọn category.")
                if current_category:
                    category_input = page.locator('label:has-text("File category") + div input').first
                    if category_input:
                        clear_btn = page.locator('label:has-text("File category") + div button[aria-label="Clear"]').first
                        if clear_btn and clear_btn.is_visible():
                            print("Đang clear trường File Category cũ...")
                            clear_btn.click()
                            time.sleep(1)
                            current_category = None
                        else:
                            print("Không tìm thấy hoặc không hiển thị nút clear File Category.")
                    else:
                        print("Không tìm thấy ô File Category.")
                else:
                    print("Trường File Category đã rỗng, không cần clear.")

        # Bắt đầu quy trình upload file
        print("=== Bắt đầu quy trình upload file ===")
        
        # 1. Click nút File upload để mở form chọn file
        print("Đang tìm nút File upload...")
        # Thử nhiều cách để tìm nút File upload
        upload_button = None
        try:
            # Cách 1: Tìm theo text trong span
            upload_button = page.locator('span.MuiTypography-root:text-is("File upload")').first
            if not upload_button:
                # Cách 2: Tìm theo class của span
                upload_button = page.locator('span.css-fyswvn:has-text("File upload")').first
            if not upload_button:
                # Cách 3: Tìm theo cấu trúc HTML đầy đủ
                upload_button = page.locator('button:has(span.MuiTypography-root.MuiTypography-body1.MuiListItemText-primary:text-is("File upload"))').first
            
            if not upload_button:
                print("Không tìm thấy nút File upload")
                return None
                
            print("Đã tìm thấy nút File upload")
            upload_button.click()
            print("Đã click nút File upload")
            time.sleep(5)  # Đợi form hiện lên đầy đủ
        except Exception as e:
            print(f"Lỗi khi tìm hoặc click nút File upload: {str(e)}")
            return None

        # 2. Tìm input file và chọn file
        print("Đang tìm input file để upload...")
        file_input = page.locator('input[type="file"]').first
        if not file_input:
            print("Không tìm thấy input file")
            return None
        print("Đã tìm thấy input file")
        
        # Set file và đợi
        try:
            print(f"Đang upload file: {file_path}")
            file_input.set_input_files(file_path)
            print("Đã chọn file để upload")
            time.sleep(5)  # Đợi file được chọn
        except Exception as e:
            print(f"Lỗi khi chọn file: {str(e)}")
            return None
        
        # 3. Click nút Upload 1 File
        print("Đang tìm nút Upload 1 File...")
        upload_file_button = page.locator('button:has-text("Upload 1 File")').first
        if not upload_file_button:
            print("Không tìm thấy nút Upload 1 File")
            return None
        print("Đã tìm thấy nút Upload 1 File")
        
        # Click nút Upload 1 File và đợi
        try:
            upload_file_button.click()
            print("Đã click nút Upload 1 File")
            time.sleep(10)  # Tăng thời gian đợi upload xong
        except Exception as e:
            print(f"Lỗi khi click nút Upload 1 File: {str(e)}")
            return None
        
        # 4. Click nút Close
        print("Đang tìm nút Close...")
        close_button = page.locator('div.MuiDialogActions-root button:has-text("Close")').first
        if not close_button:
            print("Không tìm thấy nút Close")
            return None
        print("Đã tìm thấy nút Close")
        
        # Click nút Close và đợi
        try:
            time.sleep(2)  # Đợi nút sẵn sàng
            close_button.click()
            print("Đã click nút Close")
            
            # Đợi dialog biến mất
            page.wait_for_selector('div.MuiDialogActions-root', state='hidden', timeout=30000)
            print("Dialog đã đóng")
            time.sleep(5)  # Đợi trang ổn định
            return True
        except Exception as e:
            print(f"Lỗi khi click nút Close: {str(e)}")
            return None

    except TimeoutError as e:
        print(f"Lỗi timeout: {str(e)}")
        return None
    except Exception as e:
        print(f"Lỗi không xác định: {str(e)}")
        return None

def find_file_and_get_drawing_id(page, file_name):
    """Tìm file đã upload và lấy Drawing ID"""
    try:
        print(f"\nĐang tìm file: {file_name}")
        
        # Đợi modal đóng trước khi click nút Filter
        wait_for_modal_close(page)
        
        # Click nút Filter để mở bộ lọc
        print("Đang click nút Filter...")
        filter_button = page.locator('button.MuiButtonBase-root.MuiIconButton-root:has(svg[data-testid="TuneIcon"])').first
        if filter_button:
            print("Đã tìm thấy nút Filter")
            filter_button.click()
            print("Đã click nút Filter")
            time.sleep(5)
            
            # Đợi modal đóng trước khi chọn File name
            wait_for_modal_close(page)
            
            # Chọn File name trong dropdown
            print("Đang chọn File name trong dropdown...")
            file_name_select = page.locator('#filter-field-select').first
            if file_name_select:
                file_name_select.click()
                time.sleep(2)
                file_name_option = page.locator('li.MuiMenuItem-root[data-value="fileName"]:has-text("File name")').first
                if file_name_option:
                    file_name_option.click()
                    print("Đã chọn File name")
                    time.sleep(2)
                else:
                    print("Không tìm thấy option File name")
                    return None
            else:
                print("Không tìm thấy dropdown để chọn File name")
                return None

            # Đợi modal đóng trước khi chọn contains
            wait_for_modal_close(page)

            # Chọn contains trong operation dropdown
            print("Đang chọn contains trong operation dropdown...")
            operation_select = page.locator('#filter-operation-select').first
            if operation_select:
                operation_select.click()
                time.sleep(2)
                contains_option = page.locator('li.MuiMenuItem-root[data-value="contains"]:has-text("contains")').first
                if contains_option:
                    contains_option.click()
                    print("Đã chọn contains")
                    time.sleep(2)
                else:
                    print("Không tìm thấy option contains")
                    return None
            else:
                print("Không tìm thấy dropdown để chọn operation")
                return None

            # Nhập tên file vào ô input
            print("Đang nhập tên file...")
            file_name_input = page.locator('#filter-value-input').first
            if file_name_input:
                file_name_input.fill(file_name)
                print("Đã nhập tên file")
                time.sleep(2)
            else:
                print("Không tìm thấy ô input để nhập tên file")
                return None

            # Đợi modal đóng trước khi click nút Add
            wait_for_modal_close(page)

            # Click nút Add
            print("Đang click nút Add...")
            add_button = page.locator('button.MuiButton-contained:has-text("Add")').first
            if add_button:
                add_button.click()
                print("Đã click nút Add")
                time.sleep(5)
            else:
                print("Không tìm thấy nút Add")
                return None

            # Đợi modal đóng trước khi click vào file
            wait_for_modal_close(page)

            # Tìm và click vào file trong kết quả tìm kiếm
            print("Đang tìm file trong kết quả tìm kiếm...")
            file_element = page.locator('button.MuiCardActionArea-root:has-text("File name:")').first
            if file_element:
                print("Đã tìm thấy file")
                # Đợi file element hiển thị
                file_element.wait_for(state="visible", timeout=10000)
                time.sleep(5)  # Đợi UI ổn định
                
                # Click vào file
                file_element.click()
                print("Đã click vào file")
                time.sleep(10)  # Đợi trang chi tiết load
                
                # Click vào trang chi tiết nếu cần
                detail_button = page.locator('button.MuiButton-textSecondary.MuiButton-disableElevation:has-text("DR-")').first
                if detail_button:
                    detail_button.click()
                    time.sleep(10)  # Đợi trang load
                
                # Lấy Drawing ID
                drawing_id_button = page.locator('button.MuiButton-textSecondary.MuiButton-disableElevation:has-text("DR-")').first
                if drawing_id_button:
                    drawing_id = drawing_id_button.inner_text()
                    print(f"\nĐã lấy được Drawing ID: {drawing_id}")
                    return drawing_id
                else:
                    print("Không tìm thấy Drawing ID")
                    return None
            else:
                print("Không tìm thấy file trong kết quả tìm kiếm")
                return None
        else:
            print("Không tìm thấy nút Filter")
            return None
            
    except Exception as e:
        print(f"Lỗi khi tìm file: {str(e)}")
        return None

def update_description(page, description):
    """Cập nhật Description cho file"""
    try:
        print("\nĐang cập nhật Description...")
        
        # Click vào icon Edit Description
        print("Đang tìm nút Edit Description...")
        # Tìm nút Edit Description dựa trên HTML chính xác
        edit_icon = page.locator('h2.MuiTypography-root:has-text("Description") + button.MuiIconButton-root').first
        if edit_icon:
            print("Đã tìm thấy nút Edit Description")
            edit_icon.click()
            print("Đã click vào nút Edit Description")
            time.sleep(3)

            # Nhập Description
            print("Đang nhập Description...")
            desc_input = page.locator('textarea[name="description"]').first
            if desc_input:
                print("Đã tìm thấy ô nhập Description")
                desc_input.fill(description)
                print("Đã nhập Description")
                time.sleep(2)

                # Click nút Save
                print("Đang tìm nút Save...")
                save_button = page.locator('button[type="submit"]:has-text("Save")').first
                if save_button:
                    print("Đã tìm thấy nút Save")
                    save_button.click()
                    print("Đã lưu Description")
                    time.sleep(5)
                    return True
                else:
                    print("Không tìm thấy nút Save")
            else:
                print("Không tìm thấy ô nhập Description")
        else:
            print("Không tìm thấy nút Edit Description")
            
        return False
        
    except Exception as e:
        print(f"Lỗi khi cập nhật Description: {str(e)}")
        return False
