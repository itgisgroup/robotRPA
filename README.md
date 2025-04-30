# CADDi Drawer File Upload Automation

Dự án tự động hóa quy trình upload và quản lý file trên hệ thống CADDi Drawer.

## Mô tả Dự Án

Dự án này tự động hóa các công việc sau:
1. Upload file PDF lên hệ thống CADDi Drawer
2. Cập nhật thông tin mô tả (Description) cho file
3. Lấy và lưu trữ Drawing ID
4. Quản lý trạng thái file trong Excel
5. Ghi log toàn bộ quá trình

## Cấu Trúc Thư Mục

```
robotRPA/
├── TMF-nguon/       # Thư mục chứa file nguồn cần upload
├── TMF-upload/      # Thư mục chứa file đã upload
├── TMF-completed/   # Thư mục chứa file đã xử lý hoàn tất
├── bot_caddi.py     # Module chính xử lý tương tác với CADDi
├── main_local.py    # Script chính để chạy automation
├── excel_handler.py # Module xử lý file Excel
├── logger.py        # Module ghi log
└── requirements.txt # Các dependency cần thiết
```

## Quy Trình Xử Lý

### 1. Upload File
- Đọc danh sách file từ Excel
- Kiểm tra file trong thư mục TMF-nguon
- Upload lên CADDi Drawer với Project và Category tương ứng
- Di chuyển file đã upload sang TMF-upload
- Cập nhật trạng thái trong Excel

### 2. Cập Nhật Description
- Tìm file đã upload trên CADDi Drawer
- Click vào file để mở chi tiết
- Lấy Drawing ID
- Cập nhật Description từ Excel
- Lưu thông tin

### 3. Hoàn Thành Xử Lý
- Cập nhật Drawing ID vào Excel
- Di chuyển file từ TMF-upload sang TMF-completed
- Cập nhật trạng thái "Hoàn thành" trong Excel
- Di chuyển dòng dữ liệu sang sheet hoàn thành

## Cài Đặt và Sử Dụng

### Yêu Cầu Hệ Thống
- Python 3.11+
- Playwright
- pandas
- openpyxl

### Cài Đặt
1. Clone repository:
```bash
git clone https://github.com/itgisgroup/robotRPA.git
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Cài đặt Playwright:
```bash
playwright install
```

### Cấu Hình
1. Tạo các thư mục cần thiết:
- TMF-nguon
- TMF-upload
- TMF-completed

2. Chuẩn bị file Excel với các cột:
- Tên file (File name)
- Tên dự án (Project)
- File category
- Mô tả (Description)
- Trạng thái

### Chạy Chương Trình
```bash
python main_local.py
```

## Xử Lý Lỗi và Log

### Hệ Thống Log
- Log được ghi vào file `bot.log`
- Log được lưu trong sheet "Logs" của file Excel
- Các loại log: INFO, ERROR, SUCCESS

### Xử Lý Lỗi
- Tự động retry khi không tìm thấy element
- Ghi log chi tiết cho mỗi bước xử lý
- Cập nhật trạng thái lỗi trong Excel
- Giữ nguyên file trong thư mục gốc khi có lỗi

## Bảo Mật
- Thông tin đăng nhập được lưu trong biến môi trường
- File Excel chứa dữ liệu nhạy cảm không được push lên git
- Các file đã xử lý được lưu trữ an toàn trong thư mục riêng

## Đóng Góp
Mọi đóng góp vui lòng tạo Pull Request hoặc báo lỗi qua Issues.

## License
MIT License 