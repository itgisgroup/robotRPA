# Bot Tự Động Upload File lên CADDi Drawer

Dự án này tự động hóa quy trình tải file PDF từ Google Drive lên CADDi Drawer, với tính năng theo dõi trạng thái và ghi log tự động. Bot xử lý toàn bộ quy trình từ việc đọc thông tin file từ Google Sheets, tải file từ Google Drive, upload lên CADDi Drawer và cập nhật trạng thái.

## Tính Năng

- Tự động upload file từ Google Drive lên CADDi Drawer
- Tích hợp với Google Sheets để theo dõi và cập nhật trạng thái file
- Tự động di chuyển file đã hoàn thành vào thư mục hoàn thành
- Hệ thống ghi log chi tiết
- Xử lý lỗi và cơ chế thử lại
- Tự động hóa trình duyệt sử dụng Playwright

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Dự án Google Cloud với các API đã kích hoạt:
  - Google Drive API
  - Google Sheets API
- Tài khoản CADDi Drawer
- Thông tin xác thực tài khoản dịch vụ (credentials.json)

## Cài Đặt

1. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

2. Cài đặt trình duyệt Playwright:
```bash
playwright install
```

3. Cấu hình các thông số trong `main.py`:
- `SHEET_ID`: ID của Google Sheet
- `COMPLETED_FOLDER_ID`: ID của thư mục Google Drive chứa file đã hoàn thành
- `USERNAME`: Email đăng nhập CADDi Drawer
- `PASSWORD`: Mật khẩu đăng nhập CADDi Drawer

4. Thiết lập Google Sheet với các cột sau:
- Tên dự án (Project)
- Tên file (File name)
- Mô tả (Description)
- Đường dẫn file
- ID file CADDi
- Trạng thái

## Quy Trình Chi Tiết

Bot thực hiện theo quy trình từng bước như sau:

1. **Khởi Tạo và Thiết Lập**
   - Tải cấu hình từ main.py
   - Khởi tạo hệ thống ghi log
   - Thiết lập kết nối với các API của Google

2. **Đọc Danh Sách File từ Google Sheet**
   - Kết nối đến Google Sheet đã chỉ định
   - Đọc các dòng có trạng thái "Chờ xử lý"
   - Trích xuất thông tin file (tên, dự án, mô tả, đường dẫn)

3. **Quản Lý Phiên Trình Duyệt**
   - Khởi tạo trình duyệt Playwright ở chế độ có giao diện
   - Xử lý đăng nhập CADDi Drawer
   - Duy trì phiên làm việc cho nhiều lần upload

4. **Vòng Lặp Xử Lý File**
   Với mỗi file:
   
   a. **Tải từ Google Drive**
   - Lấy ID file từ URL Google Drive
   - Tải về thư mục tạm thời
   - Kiểm tra tính toàn vẹn của file
   
   b. **Upload lên CADDi Drawer**
   - Click nút Upload
   - Chọn dự án từ danh sách thả xuống
   - Upload file
   - Đợi hoàn thành upload
   - Xử lý các hộp thoại xác nhận upload
   
   c. **Xác Minh File và Cập Nhật Mô Tả**
   - Tìm kiếm file đã upload
   - Mở chi tiết file
   - Lấy Drawing ID
   - Cập nhật mô tả file
   
   d. **Cập Nhật Trạng Thái**
   - Cập nhật Drawing ID vào Google Sheet
   - Chuyển dòng sang sheet "Upload Hoàn thành"
   - Di chuyển file vào thư mục hoàn thành trong Google Drive
   
   e. **Ghi Log**
   - Ghi lại tất cả các hành động vào bot.log
   - Cập nhật sheet log trong Google Sheets
   - Xử lý và ghi log các lỗi

5. **Xử Lý Lỗi**
   - Thử lại khi gặp lỗi mạng
   - Ghi log tất cả các lỗi
   - Duy trì trạng thái cho các lần upload thất bại
   - Cung cấp thông báo lỗi chi tiết

## Hệ Thống Ghi Log

Bot duy trì log chi tiết tại:
- File `bot.log` cho log kỹ thuật chi tiết
- Sheet "Logs" trong Google Sheets để theo dõi trạng thái thân thiện với người dùng

## Xử Lý Lỗi

Hệ thống bao gồm xử lý lỗi mạnh mẽ cho:
- Vấn đề kết nối mạng
- Lỗi tải/upload file
- Giới hạn tốc độ API Google
- Thay đổi giao diện CADDi Drawer
- Timeout phiên làm việc
- Vấn đề về định dạng/kích thước file

## Theo Dõi Trạng Thái File

File có thể có các trạng thái sau:
- Chờ xử lý
- Đang xử lý
- Hoàn thành
- Lỗi

## Hỗ Trợ

Khi gặp vấn đề, vui lòng kiểm tra:
1. File log
2. Xác thực thông tin đăng nhập API Google
3. Kiểm tra thông tin đăng nhập CADDi Drawer
4. Kiểm tra kết nối mạng
5. Kiểm tra quyền truy cập file trong Google Drive 