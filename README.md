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

## Cấu Trúc File Excel Nguồn

### 1. Yêu Cầu File Excel
- Định dạng: `.xlsx` (Excel 2007 trở lên)
- Sheet chính: "Data" (chứa dữ liệu cần xử lý)
- Sheet phụ: "Completed" (chứa dữ liệu đã xử lý)
- Sheet log: "Logs" (chứa lịch sử xử lý)

### 2. Cấu Trúc Sheet "Data"
| Cột | Mô tả | Yêu cầu | Ví dụ |
|-----|--------|---------|--------|
| File name | Tên file PDF cần upload | Bắt buộc, phải trùng với tên file trong thư mục TMF-nguon | `ABC123.pdf` |
| Project | Tên dự án trên CADDi | Bắt buộc, phải khớp chính xác với tên dự án trên CADDi | `Project A` |
| File category | Danh mục file | Bắt buộc, phải nằm trong danh sách category cho phép | `Drawing` |
| Description | Mô tả file | Bắt buộc, tối đa 500 ký tự | `Bản vẽ chi tiết phần A` |
| Status | Trạng thái xử lý | Tự động cập nhật | `Pending`, `Uploaded`, `Completed`, `Error` |
| Drawing ID | Mã bản vẽ từ CADDi | Tự động cập nhật sau khi upload | `DRW-123456` |
| Upload Date | Ngày upload | Tự động cập nhật | `2024-03-20 15:30:45` |
| Error Message | Thông báo lỗi (nếu có) | Tự động cập nhật khi có lỗi | `File not found` |

### 3. Quy Tắc Dữ Liệu
1. File name:
   - Không chứa ký tự đặc biệt (ngoại trừ dấu chấm và gạch dưới)
   - Phải có đuôi .pdf
   - Không được trùng lặp trong sheet

2. Project:
   - Phải tồn tại trên hệ thống CADDi
   - Phân biệt chữ hoa/thường
   - Không được để trống

3. File category:
   - Các giá trị cho phép:
     * Drawing (Bản vẽ)
     * Specification (Thông số kỹ thuật)
     * Report (Báo cáo)
     * Other (Khác)

4. Description:
   - Không chứa HTML hoặc script
   - Tối thiểu 10 ký tự
   - Tối đa 500 ký tự
   - Có thể chứa Unicode (tiếng Việt)

### 4. Sheet "Completed"
- Cấu trúc giống sheet "Data"
- Chứa các bản ghi đã xử lý thành công
- Tự động chuyển từ sheet "Data" sau khi hoàn thành
- Không được chỉnh sửa thủ công

### 5. Sheet "Logs"
| Cột | Mô tả |
|-----|--------|
| Timestamp | Thời gian ghi log |
| Level | Mức độ: INFO, ERROR, SUCCESS |
| Message | Nội dung log |
| File | File liên quan |
| Details | Chi tiết bổ sung |

### 6. Lưu Ý Quan Trọng
- Backup file Excel trước khi chạy script
- Không mở file Excel trong quá trình script đang chạy
- Không xóa hoặc thêm cột trong các sheet
- Không đổi tên sheet
- Kiểm tra định dạng dữ liệu trước khi chạy
- Đảm bảo tất cả file PDF được liệt kê đã có trong thư mục TMF-nguon

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

## Hướng Dẫn Cài Đặt Chi Tiết Cho Windows

### 1. Chuẩn Bị Môi Trường
1. Tải và cài đặt Python 3.11 hoặc cao hơn
   - Truy cập https://www.python.org/downloads/windows/
   - Tải phiên bản Python 3.11.x (Windows installer 64-bit)
   - Chạy file cài đặt
   - ✅ Đánh dấu "Add Python to PATH" trong quá trình cài đặt
   - Nhấn "Install Now"

2. Kiểm tra cài đặt Python
   - Mở Command Prompt (cmd)
   - Gõ lệnh: `python --version`
   - Nếu hiển thị phiên bản Python là thành công

### 2. Tải Mã Nguồn
1. Tải ZIP từ GitHub
   - Truy cập https://github.com/itgisgroup/robotRPA
   - Nhấn nút "Code" màu xanh
   - Chọn "Download ZIP"
   - Giải nén file ZIP vào thư mục mong muốn (Ví dụ: C:\robotRPA)

2. Hoặc sử dụng Git (nếu có)
   - Cài đặt Git từ https://git-scm.com/download/win
   - Mở Command Prompt
   - Di chuyển đến thư mục muốn lưu dự án
   - Chạy lệnh: `git clone https://github.com/itgisgroup/robotRPA.git`

### 3. Thiết Lập Môi Trường
1. Tạo môi trường ảo
   - Mở Command Prompt với quyền Administrator
   - Di chuyển đến thư mục dự án: `cd C:\robotRPA` (hoặc thư mục đã giải nén)
   - Tạo môi trường ảo: `python -m venv venv`
   - Kích hoạt môi trường: `venv\Scripts\activate`

2. Cài đặt thư viện
   - Đảm bảo đang ở trong môi trường ảo (có "(venv)" ở đầu dòng lệnh)
   - Chạy: `pip install -r requirements.txt`
   - Cài đặt Playwright: `playwright install`

### 4. Cấu Hình Thư Mục và File
1. Tạo cấu trúc thư mục
   - Tạo thư mục "TMF-nguon"
   - Tạo thư mục "TMF-upload"
   - Tạo thư mục "TMF-completed"

2. Chuẩn bị file Excel
   - Sao chép mẫu file Excel từ folder template (nếu có)
   - Hoặc tạo file Excel mới với các cột yêu cầu
   - Lưu file Excel vào thư mục gốc của dự án

### 5. Chạy Chương Trình
1. Kích hoạt môi trường (nếu chưa kích hoạt)
   - Mở Command Prompt
   - Di chuyển đến thư mục dự án
   - Chạy: `venv\Scripts\activate`

2. Chạy script
   - Chạy lệnh: `python main_local.py`
   - Theo dõi quá trình xử lý trong cửa sổ Command Prompt
   - Kiểm tra file log và Excel để xem kết quả

### 6. Xử Lý Sự Cố Thường Gặp
1. Lỗi "Python không được tìm thấy"
   - Kiểm tra lại việc thêm Python vào PATH
   - Thử cài đặt lại Python
   - Sử dụng đường dẫn đầy đủ đến Python

2. Lỗi khi cài đặt thư viện
   - Đảm bảo kết nối internet ổn định
   - Chạy với quyền Administrator
   - Cập nhật pip: `python -m pip install --upgrade pip`

3. Lỗi Playwright
   - Chạy lại lệnh: `playwright install`
   - Kiểm tra tường lửa và phần mềm diệt virus
   - Thử cài đặt trình duyệt thủ công

### 7. Bảo Trì và Cập Nhật
1. Cập nhật mã nguồn
   - Tải ZIP mới nhất từ GitHub
   - Hoặc chạy `git pull` nếu dùng Git

2. Cập nhật thư viện
   - Kích hoạt môi trường ảo
   - Chạy: `pip install -r requirements.txt --upgrade`

### 8. Liên Hệ Hỗ Trợ
Nếu gặp khó khăn trong quá trình cài đặt và sử dụng, vui lòng:
- Tạo issue trên GitHub
- Hoặc liên hệ trực tiếp qua email: [địa chỉ email hỗ trợ]

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