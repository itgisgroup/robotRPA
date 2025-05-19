Sử dụng đường dẫn mạng trong Python trên máy A
Trong file main_local.py, sửa như sau:
1. Chia sẻ thư mục trên máy B (Windows Server 2012)
Trên máy B:
Chuột phải vào thư mục bạn muốn chia sẻ (ví dụ: robot), chọn Properties.
Chuyển sang tab Sharing → bấm Advanced Sharing....
Tích chọn Share this folder.
Đặt tên share (ví dụ: robot), bấm Permissions để cấp quyền Full Control cho user hoặc Everyone (nếu không lo bảo mật nội bộ).
Bấm OK để lưu lại.
Lưu ý: Nếu máy A và B không cùng domain, nên cấp quyền cho Everyone để dễ thử nghiệm.
2. Lấy địa chỉ IP hoặc tên máy của máy B
Mở CMD trên máy B, gõ:
  ipconfig
Ghi lại địa chỉ IPv4 (ví dụ: 192.168.1.100).
3. Truy cập thư mục chia sẻ từ máy A
Trên máy A:
Mở File Explorer, nhập vào thanh địa chỉ:
  \\192.168.1.100\robot
Nếu được hỏi user/password, nhập user của máy B (hoặc user có quyền truy cập share).
Nếu truy cập được, bạn đã sẵn sàng dùng đường dẫn này trong Python.
4. Sử dụng đường dẫn mạng trong Python trên máy A
Trong file main_local.py, sửa như sau:
EXCEL_PATH = r"\\192.168.1.100\robot\Update_DescriptionDrawer.xlsx"
TMF_SOURCE_DIR = r"\\192.168.1.100\robot\TMF-nguon"
TMF_UPLOAD_DIR = r"\\192.168.1.100\robot\TMF-upload"
TMF_COMPLETED_DIR = r"\\192.168.1.100\robot\TMF-completed"
Lưu ý:
Dùng tiền tố r (raw string) để tránh lỗi escape ký tự.
Đảm bảo các thư mục/file này thực sự tồn tại trên máy B.
5. Lưu ý khi chạy code
Máy A phải luôn kết nối mạng LAN với máy B.
Nếu gặp lỗi permission, kiểm tra lại quyền share và NTFS trên máy B.
Nếu không truy cập được, thử map network drive trên máy A:
Chuột phải This PC → Map network drive...
Chọn ổ (ví dụ Z:), nhập đường dẫn: \\192.168.1.100\robot
Sau đó, bạn có thể dùng đường dẫn như: Z:\Update_DescriptionDrawer.xlsx trong Python.
6. Ví dụ hoàn chỉnh
Apply to chiasethumuc...
"
EXCEL_PATH = r"Z:\Update_DescriptionDrawer.xlsx"
TMF_SOURCE_DIR = r"Z:\TMF-nguon"
TMF_UPLOAD_DIR = r"Z:\TMF-upload"
TMF_COMPLETED_DIR = r"Z:\TMF-completed"
Hoặc dùng UNC path:
EXCEL_PATH = r"\\192.168.1.100\robot\Update_DescriptionDrawer.xlsx"