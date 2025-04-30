# Quy Trình Upload File lên CADDi Drawer

## Mục Tiêu
Tự động hóa quy trình upload file từ thư mục local lên phần mềm CADDi Drawer, cập nhật trạng thái và di chuyển file đã xử lý, dựa trên danh sách trong file Excel.

## Cấu Trúc Code

### 1. File Chính
```
/robotTH
├── main_local.py           # File chính điều khiển luồng xử lý cho local upload
├── bot_caddi.py           # Module xử lý tương tác với CADDi Drawer (sử dụng lại)
├── excel_handler.py        # Module xử lý đọc/ghi Excel local
└── logger.py              # Module ghi log (sử dụng lại)
```

### 2. Tái Sử Dụng Code
- **bot_caddi.py**: Giữ nguyên toàn bộ logic upload và xử lý file trên CADDi
- **logger.py**: Giữ nguyên module ghi log

### 3. Code Mới
- **main_local.py**: Thay thế main.py, xử lý luồng chính với file local
- **excel_handler.py**: Thay thế google_auth.py và update_google_sheet.py

## Quy Trình Chi Tiết

### Bước 1: Khởi Tạo
1. Khởi động trình duyệt một lần duy nhất
2. Đăng nhập vào CADDi Drawer
3. Duy trì phiên đăng nhập cho toàn bộ quá trình

### Bước 2: Đọc File Excel
1. Đọc file Excel `/Users/hlethanh486/Desktop/robotTH/Update_DescriptionDrawer.xlsx`
2. Lọc các dòng có trạng thái "Chờ xử lý"
3. Với mỗi dòng, lấy thông tin:
   - Đường dẫn file trong TMF-nguon
   - Tên dự án (Project)
   - File category
   - Mô tả (Description)

### Bước 3: Xử Lý Từng File
Với mỗi dòng trong Excel:

1. **Kiểm Tra File**
   - Xác nhận file tồn tại tại đường dẫn trong Excel
   - Validate định dạng và kích thước

2. **Upload và Xử Lý**
   - Gọi hàm `upload_to_caddi()` từ bot_caddi.py với các tham số:
     + username, password
     + project_name từ Excel
     + file_path từ Excel
     + description từ Excel
     + page (browser session được duy trì)

3. **Xử Lý Kết Quả**
   - Nếu upload thành công:
     + Lấy được drawing_id
     + Cập nhật ID vào Excel
     + Cập nhật trạng thái "Hoàn thành"
     + Di chuyển file sang TMF-upload
   - Nếu thất bại:
     + Ghi log lỗi
     + Cập nhật trạng thái "Lỗi"
     + Giữ nguyên file tại thư mục nguồn

### Bước 4: Kết Thúc
1. Lưu file Excel
2. Đóng trình duyệt
3. Tạo báo cáo tổng kết

## Module excel_handler.py

### Class ExcelHandler
```python
class ExcelHandler:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        
    def read_pending_files(self):
        """Đọc danh sách file chờ xử lý"""
        
    def update_file_status(self, file_name, status, drawing_id=None):
        """Cập nhật trạng thái và ID file"""
        
    def mark_as_completed(self, file_name, drawing_id):
        """Đánh dấu file đã hoàn thành"""
```

## Module main_local.py

### Hàm Chính
```python
def process_files():
    """Xử lý toàn bộ quy trình"""
    # Khởi tạo
    excel_handler = ExcelHandler(EXCEL_PATH)
    logger = Logger()
    
    # Khởi tạo browser session
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Login một lần
        login_to_caddi(page, USERNAME, PASSWORD)
        
        # Xử lý từng file
        for file in excel_handler.read_pending_files():
            try:
                # Upload và xử lý
                drawing_id = upload_to_caddi(
                    USERNAME, PASSWORD,
                    file["project_name"],
                    file["file_path"],
                    file["description"],
                    page
                )
                
                if drawing_id:
                    # Xử lý thành công
                    excel_handler.mark_as_completed(file["file_name"], drawing_id)
                    move_file_to_completed(file["file_path"])
                else:
                    # Xử lý thất bại
                    excel_handler.update_file_status(file["file_name"], "Lỗi")
                    
            except Exception as e:
                logger.log_error(f"Lỗi xử lý file {file['file_name']}: {str(e)}")
                excel_handler.update_file_status(file["file_name"], "Lỗi")
                
        # Đóng browser
        browser.close()
```

## Cấu Trúc File Excel
File `/Users/hlethanh486/Desktop/robotTH/Update_DescriptionDrawer.xlsx`:

### Sheet "Danh sách file cần upload"
- STT
- Tên dự án (Project)
- File category
- Đường dẫn file trong TMF-nguon
- Tên file (File name)
- Mô tả (Description)
- ID file CADDi
- Trạng thái

### Quy Tắc Xử Lý
1. Chỉ xử lý các dòng có:
   - Trạng thái "Chờ xử lý"
   - Đường dẫn file hợp lệ
   - Thông tin Project và Category đầy đủ

2. Các trạng thái và ý nghĩa:
   - "Chờ xử lý": File mới, chưa được xử lý
   - "Đang xử lý": File đang trong quá trình upload
   - "Đã upload thành công": File đã được upload lên CADDi Drawer thành công, chưa thêm mô tả và chưa lấy Drawing ID
   - "Hoàn thành": Đã hoàn tất tất cả các bước (upload + thêm mô tả + lấy Drawing ID + di chuyển file + cập nhật Excel)
   - "Lỗi": Gặp lỗi trong quá trình xử lý

3. Quy trình xử lý tuần tự:
   Bước 1 - Upload file:
   - Upload tất cả file có trạng thái "Chờ xử lý"
   - Khi bắt đầu upload: đổi trạng thái thành "Đang xử lý"
   - Sau khi upload xong thành công: đổi trạng thái thành "Đã upload thành công"
   - Chuyển file từ TMF-nguon sang TMF-upload

   Bước 2 - Xử lý sau upload:
   - Lọc tất cả file có trạng thái "Đã upload thành công"
   - Với mỗi file:
     + Tìm file trên CADDi Drawer
     + Thêm mô tả (Description)
     + Lấy Drawing ID
     + Cập nhật Drawing ID vào Excel
     + Chuyển file từ TMF-upload sang TMF-completed
     + Di chuyển dòng sang sheet "Upload Hoàn thành"
     + Đổi trạng thái thành "Hoàn thành" (chỉ khi tất cả các bước trên đều thành công)

4. Xử lý lỗi:
   - Lỗi khi upload:
     + Đổi trạng thái về "Chờ xử lý"
     + Giữ nguyên file ở TMF-nguon
   - Lỗi khi xử lý sau upload:
     + Đổi trạng thái thành "Lỗi"
     + Giữ nguyên file ở TMF-upload
     + Ghi chi tiết lỗi vào log
   - File có trạng thái "Lỗi" cần được xem xét và xử lý thủ công

# Kế Hoạch Cải Tiến Hệ Thống Upload CADDi Drawer

## Các Vấn Đề Cần Khắc Phục

### 1. Thiếu Bước Chọn File Category
- Cần thêm bước chọn File Category ngay sau khi chọn dự án
- Thực hiện trước khi upload file
- Đảm bảo phân loại file chính xác

### 2. Cập Nhật Excel Chưa Đầy Đủ
- Chưa cập nhật Drawing ID vào cột "ID file (CADDi)"
- Chưa thay đổi trạng thái thành "Hoàn thành" sau khi upload thành công
- Cần đảm bảo theo dõi tiến độ chính xác

### 3. Quản Lý Sheet Excel
- Chưa di chuyển các dòng đã hoàn thành sang sheet "Upload Hoàn thành"
- Cần tự động di chuyển sau khi xử lý xong

### 4. Di Chuyển File Trong Thư Mục
- Chưa di chuyển file từ TMF-nguon sang TMF-upload sau khi upload thành công
- Cần tự động di chuyển để theo dõi tiến độ

## Đề Xuất Cải Tiến Quy Trình

### Quy Trình Hiện Tại
1. Upload một file
2. Xử lý hoàn chỉnh (thêm mô tả, cập nhật trạng thái)
3. Chuyển sang file tiếp theo
4. Lặp lại các bước trên

### Quy Trình Đề Xuất
1. Upload tất cả file trước:
   - Chọn dự án
   - Chọn File Category
   - Upload file
   - Click "Close"
   - Lặp lại cho đến khi upload hết file

2. Xử lý hàng loạt sau khi upload xong:
   - Tìm từng file
   - Thêm mô tả
   - Cập nhật Drawing ID
   - Cập nhật trạng thái Excel
   - Di chuyển file trong thư mục

### Lợi Ích
- Giảm thời gian xử lý
- Giảm số lượng thao tác lặp lại
- Quy trình upload file liên tục, không bị gián đoạn
- Dễ dàng theo dõi và kiểm soát tiến độ

## Các Bước Triển Khai
1. Cập nhật code để thêm bước chọn File Category
2. Thêm chức năng cập nhật Excel đầy đủ
3. Phát triển tính năng di chuyển dòng giữa các sheet
4. Bổ sung chức năng di chuyển file giữa các thư mục
5. Tối ưu hóa quy trình theo đề xuất mới 

## Cải Tiến Mới - Tối Ưu Hóa Chọn Project và File Category

### 1. Vấn Đề
- Hiện tại phải chọn lại Project và File Category cho mỗi lần upload file
- Gây lãng phí thời gian khi upload nhiều file cùng Project hoặc Category
- Tăng khả năng xảy ra lỗi do thao tác thủ công nhiều lần

### 2. Giải Pháp
- Lưu trữ Project và File Category hiện tại trong biến global
- Kiểm tra và so sánh với thông tin file mới trước khi thực hiện chọn lại
- Chỉ thực hiện chọn lại khi có sự thay đổi

### 3. Chi Tiết Thực Hiện
```python
# Biến lưu trữ
current_project = None
current_category = None

# Logic kiểm tra
need_select_project = current_project != project_name
need_select_category = current_category != file_category
```

### 4. Các Trường Hợp Xử Lý
1. Trường hợp 1: Giống hoàn toàn
   - Project và Category giống file trước
   - Chỉ cần chọn file để upload
   - Tiết kiệm 2 bước thao tác

2. Trường hợp 2: Khác một thông tin
   - Chỉ khác Project: chọn lại Project + upload file
   - Chỉ khác Category: chọn lại Category + upload file
   - Tiết kiệm 1 bước thao tác

3. Trường hợp 3: Khác hoàn toàn
   - Khác cả Project và Category
   - Thực hiện đầy đủ các bước
   - Không bỏ sót thông tin

### 5. Lợi Ích
- Giảm thời gian xử lý
- Giảm số lượng thao tác thủ công
- Giảm khả năng xảy ra lỗi
- Tăng hiệu quả khi xử lý batch file
- Dễ dàng theo dõi và debug

### 6. Logging
- Ghi log rõ ràng về việc giữ nguyên hay thay đổi
- Thông báo chi tiết các bước thực hiện
- Dễ dàng phát hiện và xử lý lỗi

### 7. Kết Hợp Với Quy Trình Mới
- Upload tất cả file trước
- Tận dụng tối đa việc tái sử dụng Project và Category
- Giảm đáng kể thời gian tổng thể
- Tăng độ ổn định của quá trình upload 

# Ý NGHĨA 3 THƯ MỤC
TMF-nguon (/Users/hlethanh486/Desktop/robotTH/TMF-nguon):
Đây là thư mục nguồn (source)
Chứa các file ban đầu cần được upload lên CADDi Drawer
Khi một file mới cần upload, bạn sẽ đặt nó vào thư mục này
File trong thư mục này có trạng thái "Chờ xử lý" trong Excel
TMF-upload (/Users/hlethanh486/Desktop/robotTH/TMF-upload):
Đây là thư mục trung gian
Khi một file đã được upload thành công lên CADDi Drawer, nó sẽ được chuyển từ TMF-nguon sang thư mục này
File trong thư mục này có trạng thái "Đã upload thành công" trong Excel
File ở đây đang chờ được xử lý tiếp (thêm mô tả, lấy Drawing ID)
TMF-completed (/Users/hlethanh486/Desktop/robotTH/TMF-completed):
Đây là thư mục đích cuối cùng
Khi một file đã được xử lý hoàn tất (đã upload + đã thêm mô tả + đã có Drawing ID), nó sẽ được chuyển từ TMF-upload sang thư mục này
File trong thư mục này đã hoàn thành quy trình và được chuyển sang sheet "Upload Hoàn thành" trong Excel
Quy trình di chuyển file:
Apply to main_local.p...
)
Các hàm xử lý việc di chuyển file:
move_file_to_upload(source_path): Di chuyển file từ TMF-nguon sang TMF-upload
move_file_to_completed(upload_path): Di chuyển file từ TMF-upload sang TMF-completed
excel_handler.move_file(file_name, source_dir, dest_dir): Hàm chung để di chuyển file giữa các thư mục
Mục đích của việc phân chia thư mục như này:
Theo dõi được trạng thái xử lý của file qua vị trí của nó
Dễ dàng kiểm soát và khắc phục lỗi nếu có
Có thể chạy lại quy trình từ bất kỳ bước nào nếu cần
Giữ được file gốc an toàn trong quá trình xử lý
Bạn có thêm câu hỏi gì về cách sử dụng các thư mục này không?