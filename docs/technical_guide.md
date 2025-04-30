# Tài Liệu Kỹ Thuật - CADDi Drawer Automation

## 1. Kiến Trúc Hệ Thống

### 1.1 Tổng Quan
```
robotRPA/
├── bot_caddi.py     # Module xử lý tương tác với CADDi
├── main_local.py    # Script điều khiển chính
├── excel_handler.py # Module xử lý Excel
└── logger.py        # Module ghi log
```

### 1.2 Các Module Chính
1. **bot_caddi.py**
   - Class `CaddiBot`: Xử lý tương tác với CADDi Drawer
   - Quản lý phiên làm việc Playwright
   - Xử lý các thao tác upload và cập nhật

2. **excel_handler.py**
   - Class `ExcelHandler`: Quản lý đọc/ghi file Excel
   - Xử lý di chuyển dữ liệu giữa các sheet
   - Cập nhật trạng thái và log

3. **logger.py**
   - Class `Logger`: Quản lý ghi log
   - Ghi log vào file và Excel
   - Phân loại và định dạng log

4. **main_local.py**
   - Script điều khiển chính
   - Điều phối luồng xử lý
   - Xử lý lỗi và retry

## 2. Quy Trình Xử Lý Chi Tiết

### 2.1 Khởi Tạo
1. **Kiểm tra môi trường**
   ```python
   - Kiểm tra thư mục làm việc
   - Kiểm tra file Excel nguồn
   - Kiểm tra kết nối internet
   ```

2. **Khởi tạo các module**
   ```python
   - Khởi tạo Logger
   - Khởi tạo ExcelHandler
   - Khởi tạo CaddiBot với Playwright
   ```

### 2.2 Xử Lý File
1. **Đọc danh sách file**
   ```python
   - Đọc từ sheet "Data"
   - Lọc các file chưa xử lý (Status = "Pending")
   - Kiểm tra tồn tại file trong TMF-nguon
   ```

2. **Upload file**
   ```python
   - Đăng nhập CADDi
   - Chọn Project
   - Upload file
   - Cập nhật trạng thái "Uploaded"
   ```

3. **Cập nhật thông tin**
   ```python
   - Tìm file vừa upload
   - Cập nhật Description
   - Lấy Drawing ID
   - Cập nhật vào Excel
   ```

4. **Di chuyển file**
   ```python
   - Di chuyển file từ TMF-nguon sang TMF-upload
   - Sau khi hoàn tất, chuyển sang TMF-completed
   ```

### 2.3 Xử Lý Lỗi
1. **Retry Logic**
   ```python
   MAX_RETRIES = 3
   RETRY_DELAY = 5  # seconds
   
   def retry_operation():
       for attempt in range(MAX_RETRIES):
           try:
               # Thực hiện thao tác
               return success
           except Exception as e:
               log_error(e)
               wait(RETRY_DELAY)
   ```

2. **Các loại lỗi**
   - Network Error: Lỗi kết nối
   - File Error: Lỗi file không tồn tại/không đọc được
   - CADDi Error: Lỗi từ hệ thống CADDi
   - Excel Error: Lỗi đọc/ghi Excel

### 2.4 Logging
1. **Log Levels**
   ```python
   INFO    # Thông tin thông thường
   ERROR   # Lỗi xử lý
   SUCCESS # Xử lý thành công
   WARNING # Cảnh báo
   ```

2. **Log Format**
   ```
   [TIMESTAMP] [LEVEL] [MODULE] Message
   ```

## 3. Cấu Hình Hệ Thống

### 3.1 Yêu Cầu Phần Cứng
- CPU: 2 cores trở lên
- RAM: Tối thiểu 4GB
- Disk: 1GB free space
- Network: Stable connection

### 3.2 Yêu Cầu Phần Mềm
- Python 3.11+
- Playwright
- pandas
- openpyxl
- Windows 10/11

### 3.3 Biến Môi Trường
```python
CADDI_USERNAME=your_username
CADDI_PASSWORD=your_password
EXCEL_PATH=path_to_excel
LOG_LEVEL=INFO
```

## 4. Quy Trình Vận Hành

### 4.1 Khởi Động
1. Kiểm tra môi trường
   ```bash
   python check_environment.py
   ```

2. Khởi động script
   ```bash
   python main_local.py
   ```

### 4.2 Giám Sát
1. **Theo dõi logs**
   - Kiểm tra file `bot.log`
   - Xem sheet "Logs" trong Excel
   - Kiểm tra console output

2. **Kiểm tra tiến độ**
   - Sheet "Data": Số file đang xử lý
   - Sheet "Completed": Số file đã hoàn thành
   - Thư mục TMF-completed

### 4.3 Xử Lý Sự Cố
1. **Script dừng đột ngột**
   - Kiểm tra logs
   - Restart script
   - Kiểm tra trạng thái file trong Excel

2. **Lỗi upload file**
   - Kiểm tra kết nối mạng
   - Kiểm tra phiên đăng nhập CADDi
   - Thử upload lại file lỗi

3. **Lỗi Excel**
   - Backup file Excel
   - Đóng tất cả instance Excel
   - Restart script

## 5. Bảo Trì và Nâng Cấp

### 5.1 Backup
1. **Backup dữ liệu**
   ```bash
   # Backup Excel
   cp data.xlsx data_backup_YYYYMMDD.xlsx
   
   # Backup logs
   cp bot.log bot_YYYYMMDD.log
   ```

2. **Backup code**
   ```bash
   git commit -am "Backup before update"
   git push
   ```

### 5.2 Cập Nhật
1. **Cập nhật code**
   ```bash
   git pull
   pip install -r requirements.txt --upgrade
   ```

2. **Kiểm tra sau cập nhật**
   - Chạy test cases
   - Kiểm tra logs
   - Thử nghiệm với file mẫu

## 6. Phụ Lục

### 6.1 Mã Lỗi
| Mã | Mô tả | Cách xử lý |
|-----|--------|------------|
| E001 | Lỗi kết nối | Kiểm tra mạng |
| E002 | File không tồn tại | Kiểm tra thư mục |
| E003 | Lỗi đăng nhập | Kiểm tra credentials |
| E004 | Lỗi Excel | Đóng file Excel |

### 6.2 Thông Số Kỹ Thuật
- Thời gian xử lý trung bình: 2-3 phút/file
- Số lượng file xử lý đồng thời: 1
- Dung lượng file tối đa: 100MB
- Định dạng file hỗ trợ: PDF

### 6.3 Liên Hệ Hỗ Trợ
- Technical Support: biz@satavan.vn
- Emergency Contact: 0909099580
- GitHub Issues: 