from playwright.sync_api import sync_playwright, TimeoutError
import time
import os

CADDI_URL = "https://caddi-drawer.com/en/22c37f66-ee3f-4af4-ab92-16c305be7460"

def upload_to_caddi(username, password, project_name, file_path, description):
    print(f"\nTên dự án từ Google Sheet: {project_name}")
    print(f"Đường dẫn file cần upload: {file_path}")
    print(f"Tên file: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
        return None
        
    print(f"Kích thước file: {os.path.getsize(file_path)} bytes")
    
    with sync_playwright() as p:
        try:
            print("Khởi tạo trình duyệt...")
            browser = p.chromium.launch(
                headless=False,
                slow_mo=100
            )
            print("Đã khởi tạo trình duyệt thành công")
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            print("Đã tạo context mới")
            
            page = context.new_page()
            print("Đã tạo trang mới")
            
            page.set_default_timeout(120000)  # Tăng timeout lên 120 giây
            print("Đã set timeout")

            print("Đang truy cập trang CADDi...")
            page.goto(CADDI_URL)
            print("Đã load xong trang CADDi")
            
            # Đợi trang load xong
            print("Đang đợi trang load hoàn tất...")
            time.sleep(10)
            
            print("Đang tìm form đăng nhập...")
            # Tìm và điền username
            username_input = page.locator('input[type="text"]').first
            if username_input:
                print("Đã tìm thấy ô username")
                username_input.fill(username)
                print("Đã nhập username")
                time.sleep(2)
            else:
                print("Không tìm thấy ô username")
            
            # Tìm và điền password
            password_input = page.locator('input[type="password"]').first
            if password_input:
                print("Đã tìm thấy ô password")
                password_input.fill(password)
                print("Đã nhập password")
                time.sleep(2)
            else:
                print("Không tìm thấy ô password")
            
            print("Đang tìm nút đăng nhập...")
            # Tìm và click nút đăng nhập
            submit_button = page.locator('button[type="submit"]').first
            if submit_button:
                print("Đã tìm thấy nút đăng nhập")
                submit_button.click()
                print("Đã click nút đăng nhập")
            else:
                print("Không tìm thấy nút đăng nhập")
            
            # Chờ đăng nhập thành công và load trang chủ
            print("Đang đợi đăng nhập và load trang chủ...")
            time.sleep(15)

            # Tìm và click nút Upload ở góc phải
            print("Đang tìm nút Upload ở góc phải...")
            upload_button = page.locator('button:has-text("Upload")').first
            if upload_button:
                print("Đã tìm thấy nút Upload")
                upload_button.click()
                print("Đã click nút Upload")
                time.sleep(5)  # Chờ form upload hiện lên
            else:
                print("Không tìm thấy nút Upload")
                return None

            # Tìm và nhập tên dự án vào ô Project
            print("Đang tìm ô Project...")
            # Thử nhiều cách khác nhau để tìm ô Project
            project_selectors = [
                'label:has-text("Project") + div input',  # Tìm theo label và input
                'div.MuiAutocomplete-root input',         # Tìm theo class Autocomplete
                'div.MuiTextField-root input',           # Tìm theo class TextField
                'input[role="combobox"]'                 # Tìm theo role
            ]
            
            project_input = None
            for selector in project_selectors:
                project_input = page.locator(selector).first
                if project_input:
                    print(f"Đã tìm thấy ô Project với selector: {selector}")
                    break
            
            if project_input:
                print("Đã tìm thấy ô Project")
                print(f"Đang nhập tên dự án: {project_name}")
                # Click vào ô input để focus
                project_input.click()
                time.sleep(1)
                # Xóa nội dung cũ nếu có
                project_input.fill("")
                time.sleep(1)
                # Nhập tên dự án mới
                project_input.fill(project_name)
                print("Đã nhập tên dự án")
                time.sleep(5)  # Chờ kết quả tìm kiếm
                
                # Click chọn dự án từ kết quả tìm kiếm
                print("Đang tìm dự án trong kết quả tìm kiếm...")
                # Thử nhiều cách khác nhau để tìm dự án
                result_selectors = [
                    f'div:has-text("{project_name}")',
                    f'div[class*="project"]:has-text("{project_name}")',
                    f'div[class*="item"]:has-text("{project_name}")',
                    f'div[class*="option"]:has-text("{project_name}")'
                ]
                
                project_found = False
                for selector in result_selectors:
                    project_option = page.locator(selector).first
                    if project_option:
                        print(f"Đã tìm thấy dự án với selector: {selector}")
                        project_option.click()
                        print("Đã chọn dự án")
                        project_found = True
                        break
                
                if not project_found:
                    print("Không tìm thấy dự án trong kết quả tìm kiếm")
                    print("Các kết quả tìm kiếm hiện tại:")
                    search_results = page.locator('div:has-text("")').all()
                    for result in search_results:
                        print(f"- {result.inner_text()}")
                    return None
                
                time.sleep(5)  # Chờ sau khi chọn dự án
            else:
                print("Không tìm thấy ô Project")
                return None

            # Upload file
            print("Đang tìm input file để upload...")
            file_input = page.locator('input[type="file"]').first
            if file_input:
                print("Đã tìm thấy input file")
                print(f"Đang upload file: {file_path}")
                file_input.set_input_files(file_path)
                print("Đã chọn file để upload")
                time.sleep(5)  # Chờ file được chọn
                
                # Click nút Upload 1 File để bắt đầu upload
                print("Đang tìm nút Upload 1 File...")
                upload_file_button = page.locator('button:has-text("Upload 1 File")').first
                if upload_file_button:
                    print("Đã tìm thấy nút Upload 1 File")
                    upload_file_button.click()
                    print("Đã click nút Upload 1 File")
                    time.sleep(15)  # Chờ file upload xong
                    
                    # Click nút Close để đóng dialog
                    print("Đang tìm nút Close...")
                    # Đợi nút Close xuất hiện
                    try:
                        close_button = page.wait_for_selector('div.MuiDialogActions-root button:has-text("Close")', timeout=30000)
                        if close_button:
                            print("Đã tìm thấy nút Close")
                            time.sleep(2)  # Đợi thêm để đảm bảo nút đã sẵn sàng
                            close_button.click()
                            print("Đã click nút Close")
                            # Đợi dialog biến mất
                            page.wait_for_selector('div.MuiDialogActions-root', state='hidden', timeout=30000)
                            print("Dialog đã đóng")
                            time.sleep(5)  # Đợi thêm để đảm bảo trang ổn định
                        else:
                            print("Không tìm thấy nút Close")
                            return None
                    except Exception as e:
                        print(f"Lỗi khi xử lý nút Close: {str(e)}")
                        return None
                else:
                    print("Không tìm thấy nút Upload 1 File")
                    return None
            else:
                print("Không tìm thấy input file")
                return None

            # Tìm file vừa upload theo tên
            print("Đang tìm file vừa upload...")
            file_name = os.path.basename(file_path)
            
            # Click nút Filter để mở bộ lọc
            print("Đang click nút Filter...")
            # Đợi trang load hoàn tất
            time.sleep(10)  # Tăng thời gian chờ lên 10 giây
            
            # Thử tìm nút Filter
            try:
                # Tìm nút Filter bằng class và icon
                filter_button = page.locator('button.MuiButtonBase-root.MuiIconButton-root:has(svg[data-testid="TuneIcon"])').first
                if filter_button:
                    print("Đã tìm thấy nút Filter")
                    # Đợi nút có thể click được
                    filter_button.wait_for(state="visible", timeout=10000)
                    # Click nút
                    filter_button.click(force=True)  # Thêm force=True để bắt buộc click
                    print("Đã click nút Filter")
                    time.sleep(5)  # Tăng thời gian chờ sau khi click
                    
                    # Kiểm tra xem dropdown đã hiện ra chưa
                    if not page.locator('#filter-field-select').is_visible():
                        print("Dropdown chưa hiện ra, thử click lại...")
                        # Thử click bằng JavaScript
                        page.evaluate('document.querySelector("button.MuiButtonBase-root.MuiIconButton-root svg[data-testid=\'TuneIcon\']").closest("button").click()')
                        time.sleep(5)  # Tăng thời gian chờ sau khi click
                        
                        if not page.locator('#filter-field-select').is_visible():
                            print("Vẫn không thể mở dropdown")
                            return None
                    
                    print("Đã mở được dropdown Filter")
                    time.sleep(5)  # Tăng thời gian chờ sau khi mở dropdown

                    # Chọn File name trong dropdown
                    print("Đang chọn File name trong dropdown...")
                    file_name_select = page.locator('#filter-field-select').first
                    if file_name_select:
                        file_name_select.click()
                        time.sleep(2)
                        # Chọn option File name với selector chính xác hơn
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

                    # Chọn contains trong operation dropdown
                    print("Đang chọn contains trong operation dropdown...")
                    operation_select = page.locator('#filter-operation-select').first
                    if operation_select:
                        operation_select.click()
                        time.sleep(2)
                        # Chọn option contains với selector chính xác hơn
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

                    # Click nút Add
                    print("Đang click nút Add...")
                    add_button = page.locator('button.MuiButton-contained:has-text("Add")').first
                    if add_button:
                        add_button.click()
                        print("Đã click nút Add")
                        time.sleep(5)  # Đợi kết quả tìm kiếm
                    else:
                        print("Không tìm thấy nút Add")
                        return None

                else:
                    print("Không tìm thấy nút Filter")
                    return None
                
            except Exception as e:
                print(f"Lỗi khi xử lý nút Filter: {str(e)}")
                return None

            # Tìm và click vào file trong kết quả tìm kiếm
            print("Đang tìm file trong kết quả tìm kiếm...")
            # Tìm file dựa trên HTML mới
            file_element = page.locator('button.MuiCardActionArea-root:has-text("File name:")').first
                    
            if file_element:
                print("Đã tìm thấy file")
                try:
                    # Đợi file có thể click được
                    file_element.wait_for(state="visible", timeout=10000)
                    
                    # Đợi thêm để đảm bảo trang đã ổn định
                    time.sleep(5)
                    
                    # Click vào file
                    file_element.click()
                    print("Đã click vào file")
                    
                    # Đợi trang chi tiết load xong
                    time.sleep(10)
                    
                    # Kiểm tra xem đã vào trang chi tiết chưa
                    if not page.locator('button.MuiButton-textSecondary.MuiButton-disableElevation:has-text("DR-")').is_visible():
                        print("Chưa vào được trang chi tiết, thử click lại...")
                        file_element.click()
                        time.sleep(10)
                except Exception as e:
                    print(f"Lỗi khi click vào file: {str(e)}")
                    return None
            else:
                print("Không tìm thấy file trong kết quả tìm kiếm")
                return None

            # Lấy Drawing ID
            print("Đang lấy Drawing ID...")
            drawing_id_button = page.locator('button.MuiButton-textSecondary.MuiButton-disableElevation:has-text("DR-")').first
            if drawing_id_button:
                drawing_id = drawing_id_button.inner_text()
                print(f"Đã lấy được Drawing ID: {drawing_id}")
                
                # Click vào icon Edit Description
                print("Đang tìm nút Edit Description...")
                edit_icon = page.locator('button.MuiIconButton-root:has(svg[data-testid="EditOutlinedIcon"])').first
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
                            return drawing_id
                        else:
                            print("Không tìm thấy nút Save")
                    else:
                        print("Không tìm thấy ô nhập Description")
                else:
                    print("Không tìm thấy nút Edit Description")
            else:
                print("Không tìm thấy Drawing ID")
            return None

        except TimeoutError as e:
            print(f"Lỗi timeout: {str(e)}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")
            return None
        finally:
            try:
                context.close()
                browser.close()
                print("Đã đóng trình duyệt")
            except:
                print("Lỗi khi đóng trình duyệt")
