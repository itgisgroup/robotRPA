# HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY ROBOT CADDI TRÊN WINDOWS

## 1. Cài đặt Python
- Tải Python 3.11 hoặc 3.12 từ [python.org/downloads](https://www.python.org/downloads/)
- Trong quá trình cài đặt, **tích chọn "Add Python to PATH"**
- Kiểm tra cài đặt:
  ```powershell
  python --version
  pip --version
  ```

## 2. Clone code từ GitHub:https://github.com/itgisgroup/robotRPA
- Mở PowerShell hoặc CMD
- Di chuyển đến thư mục bạn muốn chứa project:
  ```powershell
  cd C:\Users\<TenUser>\Desktop
  ```
- Clone repository:
  ```powershell
  git clone <repo-url>
  cd <ten-thu-muc-project>
  ```

## 3. Tạo môi trường ảo
```powershell
python -m venv venv
.\venv\Scripts\Activate
```
Khi thành công, bạn sẽ thấy `(venv)` ở đầu dòng lệnh.

## 4. Cài đặt các thư viện cần thiết
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
**Lưu ý:**
- Nếu file `requirements.txt` có dòng `shutil==1.7.0` thì hãy mở file này và xóa dòng đó đi.

## 5. Cài đặt Playwright browsers
```powershell
playwright install
```

## 6. Chạy script
```powershell
python main_local.py
```

## 7. Tạo file .bat để chạy script tự động
- Mở Notepad, dán nội dung sau:
  ```bat
  @echo off
  cd /d %~dp0
  call venv\Scripts\activate
  python main_local.py
  pause
  ```
- Lưu với tên: `run_robot.bat` trong thư mục project (cùng cấp với `main_local.py`).

## 8. Tạo shortcut ra Desktop
- Chuột phải vào file `run_robot.bat` → **Send to** → **Desktop (create shortcut)**
- Đổi tên shortcut ngoài Desktop cho dễ nhớ, ví dụ: **Chạy Robot CADDI**

## 9. Hướng dẫn sử dụng cho user
- Double-click vào shortcut ngoài Desktop để chạy robot.
- Nếu gặp lỗi, cửa sổ sẽ không tự tắt, user có thể chụp lại màn hình lỗi gửi cho người quản trị.

## 10. Lưu ý
- Không mở file Excel khi script đang chạy.
- Đảm bảo đã cài Python, đã tạo môi trường ảo và cài đủ thư viện trước khi chạy.
- Nếu gặp lỗi thiếu thư viện, cài thêm bằng:
  ```powershell
  pip install <ten-thu-vien>
  ```
- Nếu muốn chạy bằng `python3`, đổi dòng `python main_local.py` thành `python3 main_local.py` trong file .bat.

---
**Nếu gặp lỗi nào, hãy copy thông báo lỗi và gửi lại để được hỗ trợ chi tiết hơn!** 