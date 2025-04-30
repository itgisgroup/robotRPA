# Hướng Dẫn Cài Đặt Thư Viện

## 1. Cài Đặt Môi Trường Cơ Bản

### 1.1 Cài Đặt Python
1. Tải Python 3.11+ từ [python.org](https://www.python.org/downloads/)
2. Trong quá trình cài đặt, đảm bảo tích chọn "Add Python to PATH"
3. Kiểm tra cài đặt:
   ```bash
   python --version
   pip --version
   ```

### 1.2 Tạo Môi Trường Ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## 2. Cài Đặt Cho Môi Trường Production

### 2.1 Cài Đặt Thư Viện Production
```bash
# Cài đặt từ requirements production
pip install -r requirements/requirements-prod.txt

# Cài đặt Playwright browsers
playwright install
```

### 2.2 Kiểm Tra Cài Đặt
```bash
# Kiểm tra Playwright
playwright --version

# Kiểm tra pandas
python -c "import pandas; print(pandas.__version__)"
```

## 3. Cài Đặt Cho Môi Trường Development

### 3.1 Cài Đặt Thư Viện Development
```bash
# Cài đặt từ requirements development (bao gồm cả prod)
pip install -r requirements/requirements-dev.txt

# Cài đặt pre-commit hooks
pre-commit install
```

### 3.2 Cấu Hình Công Cụ Development
```bash
# Cấu hình Black
black --version
black .

# Cấu hình Flake8
flake8 --version
flake8 .

# Cấu hình MyPy
mypy --version
mypy .
```

## 4. Xử Lý Lỗi Thường Gặp

### 4.1 Lỗi Cài Đặt Playwright
```bash
# Nếu gặp lỗi permission
sudo playwright install

# Nếu cần cài đặt dependencies
sudo apt-get install -y libgbm-dev  # Ubuntu/Debian
```

### 4.2 Lỗi Thư Viện Python
```bash
# Cập nhật pip
python -m pip install --upgrade pip

# Xóa cache pip
pip cache purge

# Cài đặt lại với verbose
pip install -v -r requirements/requirements-prod.txt
```

## 5. Kiểm Tra Cài Đặt

### 5.1 Kiểm Tra Môi Trường Production
```bash
# Chạy script kiểm tra
python scripts/check_environment.py

# Kiểm tra kết nối
python scripts/test_connection.py
```

### 5.2 Kiểm Tra Môi Trường Development
```bash
# Chạy tests
pytest

# Kiểm tra code quality
black . --check
flake8 .
mypy .
```

## 6. Cập Nhật Thư Viện

### 6.1 Cập Nhật Production
```bash
# Cập nhật tất cả packages
pip install -r requirements/requirements-prod.txt --upgrade

# Cập nhật Playwright
playwright install --force
```

### 6.2 Cập Nhật Development
```bash
# Cập nhật tất cả packages development
pip install -r requirements/requirements-dev.txt --upgrade

# Cập nhật pre-commit hooks
pre-commit autoupdate
```

## 7. Lưu Ý Quan Trọng

### 7.1 Bảo Mật
- Không commit file `.env` lên git
- Sử dụng biến môi trường cho credentials
- Kiểm tra security advisories của các package

### 7.2 Performance
- Sử dụng pip-tools để quản lý dependencies
- Định kỳ cập nhật các package
- Kiểm tra compatibility giữa các package

### 7.3 Troubleshooting
- Kiểm tra logs trong `logs/`
- Xem error messages trong console
- Tham khảo documentation của từng package

## 8. Liên Hệ Hỗ Trợ
- Technical Support: biz@satavan.vn
- Emergency Contact: 0909099580
- GitHub Issues: [repository-url] 

## 9. Quy Trình Chạy Dự Án và Xử Lý File

### 9.1 Chuẩn Bị Trước Khi Chạy
1. **Kiểm tra cấu trúc thư mục**
   ```
   robotRPA/
   ├── TMF-nguon/     # Chứa file PDF cần xử lý
   ├── TMF-upload/    # File đã upload
   └── TMF-completed/ # File đã hoàn thành
   ```

2. **Chuẩn bị file Excel**
   - Mở file Excel mẫu
   - Điền thông tin các file cần xử lý vào sheet "Data"
   - Lưu và đóng file Excel
   - Đảm bảo không có instance Excel nào đang mở file

3. **Kiểm tra file PDF**
   - Copy tất cả file PDF cần xử lý vào thư mục `TMF-nguon`
   - Đảm bảo tên file khớp với danh sách trong Excel
   - Kiểm tra file không bị lỗi/corrupt

4. **Kiểm tra môi trường**
   - Đảm bảo đã kích hoạt môi trường ảo:
     ```bash
     # Windows
     venv\Scripts\activate
     
     # Linux/Mac
     source venv/bin/activate
     ```
   - Kiểm tra kết nối internet
   - Kiểm tra đăng nhập CADDi còn hiệu lực

### 9.2 Quy Trình Chạy
1. **Khởi động script**
   ```bash
   # Di chuyển đến thư mục dự án
   cd path/to/robotRPA

   # Chạy script chính
   python main_local.py
   ```

2. **Giám sát quá trình**
   - Theo dõi console log
   - Kiểm tra file `bot.log`
   - Quan sát sheet "Logs" trong Excel
   - Kiểm tra các thư mục TMF-upload và TMF-completed

3. **Xử lý trong quá trình chạy**
   - KHÔNG mở file Excel
   - KHÔNG di chuyển/đổi tên file trong các thư mục TMF
   - KHÔNG tắt terminal đang chạy script
   - Nếu cần dừng, sử dụng Ctrl+C và đợi script dừng hoàn toàn

### 9.3 Kiểm Tra Kết Quả
1. **Kiểm tra file Excel**
   - Mở sheet "Data": Kiểm tra trạng thái các file
   - Mở sheet "Completed": Xem các file đã xử lý
   - Mở sheet "Logs": Kiểm tra có lỗi không

2. **Kiểm tra thư mục**
   - `TMF-nguon`: Không còn file nào
   - `TMF-upload`: Chứa file đang xử lý
   - `TMF-completed`: Chứa file đã hoàn thành

3. **Kiểm tra trên CADDi**
   - Đăng nhập vào CADDi
   - Kiểm tra các file đã upload
   - Xác nhận thông tin Description và Drawing ID

### 9.4 Xử Lý Lỗi
1. **Lỗi upload file**
   - Kiểm tra log để xác định nguyên nhân
   - File vẫn ở thư mục `TMF-nguon`
   - Trạng thái trong Excel là "Error"
   - Thử upload lại file đó

2. **Lỗi cập nhật thông tin**
   - File đã chuyển sang `TMF-upload`
   - Kiểm tra thông tin trên CADDi
   - Có thể cập nhật thủ công nếu cần

3. **Script dừng đột ngột**
   - Kiểm tra và ghi chú file đang xử lý
   - Đóng tất cả instance Excel
   - Chạy lại script

### 9.5 Hoàn Thành Xử Lý
1. **Backup dữ liệu**
   ```bash
   # Backup file Excel
   cp data.xlsx backup/data_YYYYMMDD.xlsx
   
   # Backup logs
   cp bot.log backup/bot_YYYYMMDD.log
   ```

2. **Kiểm tra cuối cùng**
   - Tất cả file đã được xử lý
   - Không còn lỗi trong logs
   - Sheet "Completed" đã cập nhật đầy đủ

3. **Dọn dẹp**
   - Có thể xóa file trong `TMF-completed` (sau khi đã backup)
   - Archive các file log cũ
   - Dọn dẹp cache nếu cần

### 9.6 Lưu Ý Quan Trọng
1. **Trước khi chạy**
   - Backup file Excel
   - Kiểm tra dung lượng ổ đĩa
   - Đảm bảo không có tác vụ khác đang chạy

2. **Trong khi chạy**
   - Không tương tác với các thư mục TMF
   - Không mở file Excel
   - Để script chạy trong terminal riêng

3. **Sau khi chạy**
   - Lưu trữ logs
   - Backup dữ liệu
   - Ghi chú các vấn đề gặp phải 

## 10. Hướng Dẫn Chi Tiết Chạy Script Trên Windows

### 10.1 Chuẩn Bị Môi Trường Windows
1. **Mở Command Prompt với quyền Administrator**
   - Nhấn Windows + X
   - Chọn "Windows Terminal (Admin)" hoặc "Command Prompt (Admin)"
   - Hoặc tìm cmd trong Start Menu, click phải và chọn "Run as administrator"

2. **Di chuyển đến thư mục dự án**
   ```cmd
   # Ví dụ thư mục cài đặt ở ổ D
   D:
   cd D:\robotRPA
   
   # Hoặc nếu ở ổ C
   C:
   cd C:\Users\TenUser\Desktop\robotRPA
   ```

### 10.2 Kích Hoạt Môi Trường
1. **Kích hoạt môi trường ảo**
   ```cmd
   # Kích hoạt môi trường
   venv\Scripts\activate
   
   # Màn hình sẽ hiển thị
   (venv) D:\robotRPA>
   ```

2. **Kiểm tra môi trường**
   ```cmd
   # Kiểm tra Python
   python --version
   
   # Kiểm tra pip
   pip list
   
   # Kiểm tra Playwright
   playwright --version
   ```

### 10.3 Kiểm Tra Trước Khi Chạy
1. **Kiểm tra thư mục và file**
   ```cmd
   # Kiểm tra cấu trúc thư mục
   dir
   
   # Kiểm tra thư mục TMF
   dir TMF-nguon
   dir TMF-upload
   dir TMF-completed
   ```

2. **Kiểm tra file Excel**
   ```cmd
   # Đảm bảo file Excel tồn tại
   dir *.xlsx
   
   # Kiểm tra quyền truy cập
   icacls data.xlsx
   ```

### 10.4 Chạy Script
1. **Chạy với chế độ thông thường**
   ```cmd
   # Chạy script chính
   python main_local.py
   ```

2. **Chạy với chế độ debug (nếu cần)**
   ```cmd
   # Chạy với flag debug
   python main_local.py --debug
   
   # Hoặc với biến môi trường
   set LOG_LEVEL=DEBUG
   python main_local.py
   ```

3. **Chạy với output chi tiết**
   ```cmd
   # Lưu output vào file
   python main_local.py > output.log 2>&1
   ```

### 10.5 Giám Sát Quá Trình
1. **Theo dõi logs trực tiếp**
   ```cmd
   # Mở terminal mới và xem log realtime
   type bot.log
   
   # Hoặc theo dõi liên tục
   tail -f bot.log
   ```

2. **Kiểm tra trạng thái**
   ```cmd
   # Kiểm tra số file trong các thư mục
   dir /b /a-d TMF-nguon | find /c /v ""
   dir /b /a-d TMF-upload | find /c /v ""
   dir /b /a-d TMF-completed | find /c /v ""
   ```

### 10.6 Xử Lý Khi Gặp Lỗi
1. **Lỗi Permission**
   ```cmd
   # Kiểm tra quyền thư mục
   icacls TMF-nguon
   icacls TMF-upload
   icacls TMF-completed
   
   # Cấp quyền nếu cần
   icacls TMF-nguon /grant Users:F
   ```

2. **Lỗi Excel đang mở**
   ```cmd
   # Kiểm tra process Excel
   tasklist | findstr "EXCEL"
   
   # Đóng Excel nếu cần
   taskkill /F /IM EXCEL.EXE
   ```

3. **Lỗi môi trường**
   ```cmd
   # Reset môi trường ảo
   deactivate
   venv\Scripts\activate
   
   # Cài lại thư viện nếu cần
   pip install -r requirements/requirements-prod.txt
   ```

### 10.7 Hoàn Thành và Dọn Dẹp
1. **Backup dữ liệu**
   ```cmd
   # Tạo thư mục backup
   mkdir backup
   
   # Copy file Excel và log
   copy data.xlsx backup\data_%date:~-4,4%%date:~-10,2%%date:~-7,2%.xlsx
   copy bot.log backup\bot_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log
   ```

2. **Dọn dẹp cache**
   ```cmd
   # Xóa file tạm
   del /Q *.tmp
   
   # Xóa cache Python
   pip cache purge
   ```

3. **Đóng môi trường**
   ```cmd
   # Thoát môi trường ảo
   deactivate
   ```

### 10.8 Các Lệnh Hữu Ích
```cmd
# Kiểm tra process đang chạy
tasklist | findstr "python"

# Kiểm tra port đang sử dụng
netstat -ano | findstr "LISTENING"

# Kiểm tra dung lượng ổ đĩa
wmic logicaldisk get size,freespace,caption

# Tạo file test
echo %date% %time% > test.log

# Kiểm tra kết nối mạng
ping google.com -n 4
``` 