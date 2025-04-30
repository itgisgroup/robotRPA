# Hướng Dẫn Đóng Gói và Tạo GUI

## 1. Tạo Giao Diện GUI

### 1.1 Cài Đặt Thư Viện
```bash
# Thư viện cho GUI
pip install PyQt6==6.6.1
pip install qt-material==2.14
pip install pyinstaller==6.3.0
```

### 1.2 Cấu Trúc GUI
```python
# main_gui.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from qt_material import apply_stylesheet

class CADDiUploaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CADDi File Uploader")
        self.setMinimumSize(800, 600)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Excel file section
        excel_group = QGroupBox("Excel File")
        excel_layout = QHBoxLayout()
        self.excel_path = QLineEdit()
        browse_excel = QPushButton("Browse")
        excel_layout.addWidget(self.excel_path)
        excel_layout.addWidget(browse_excel)
        excel_group.setLayout(excel_layout)
        
        # TMF folders section
        tmf_group = QGroupBox("TMF Folders")
        tmf_layout = QFormLayout()
        self.tmf_source = QLineEdit()
        self.tmf_upload = QLineEdit()
        self.tmf_complete = QLineEdit()
        tmf_layout.addRow("Source:", self.tmf_source)
        tmf_layout.addRow("Upload:", self.tmf_upload)
        tmf_layout.addRow("Complete:", self.tmf_complete)
        tmf_group.setLayout(tmf_layout)
        
        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_text)
        progress_group.setLayout(progress_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Upload")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        
        # Add all components to main layout
        layout.addWidget(excel_group)
        layout.addWidget(tmf_group)
        layout.addWidget(progress_group)
        layout.addLayout(button_layout)
```

### 1.3 Kết Nối Logic
```python
# Kết nối GUI với bot_caddi.py
class CADDiUploaderLogic(QObject):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.bot = CaddiBot()
        self.excel_handler = ExcelHandler()
        
    def start_upload(self, excel_path, tmf_source):
        try:
            # Khởi tạo xử lý
            self.excel_handler.load_file(excel_path)
            files = self.excel_handler.get_pending_files()
            
            # Xử lý từng file
            for i, file in enumerate(files):
                self.status_updated.emit(f"Processing {file}")
                self.bot.upload_file(file)
                progress = int((i + 1) * 100 / len(files))
                self.progress_updated.emit(progress)
                
        except Exception as e:
            self.status_updated.emit(f"Error: {str(e)}")
```

## 2. Đóng Gói Executable

### 2.1 Cấu Trúc Project
```
robotRPA/
├── src/
│   ├── main_gui.py
│   ├── bot_caddi.py
│   ├── excel_handler.py
│   └── logger.py
├── resources/
│   ├── icons/
│   └── styles/
├── build/
└── dist/
```

### 2.2 File Spec cho PyInstaller
```python
# robot_uploader.spec
block_cipher = None

a = Analysis(
    ['src/main_gui.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('resources/icons', 'icons'),
        ('resources/styles', 'styles')
    ],
    hiddenimports=[
        'PyQt6',
        'playwright',
        'pandas',
        'openpyxl'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CADDi Uploader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/app.ico'
)
```

### 2.3 Build Command
```bash
# Build executable
pyinstaller robot_uploader.spec --clean

# Hoặc build trực tiếp
pyinstaller --name="CADDi Uploader" ^
            --windowed ^
            --icon=resources/icons/app.ico ^
            --add-data="resources/icons;icons" ^
            --add-data="resources/styles;styles" ^
            src/main_gui.py
```

## 3. Cấu Trúc Triển Khai

### 3.1 Package Cài Đặt
```
CADDi Uploader/
├── CADDi Uploader.exe
├── config/
│   └── settings.ini
├── templates/
│   └── data_template.xlsx
└── README.txt
```

### 3.2 File Cấu Hình
```ini
# settings.ini
[Paths]
ExcelTemplate=templates/data_template.xlsx
TMFSource=TMF-nguon
TMFUpload=TMF-upload
TMFComplete=TMF-completed

[CADDi]
URL=https://drawer.caddi.jp
Timeout=30

[Logging]
Level=INFO
File=logs/bot.log
```

## 4. Hướng Dẫn Sử Dụng

### 4.1 Cài Đặt
1. Giải nén package vào thư mục mong muốn
2. Chạy file `CADDi Uploader.exe`
3. Nhập thông tin đăng nhập CADDi lần đầu

### 4.2 Quy Trình Sử Dụng
1. Click "Browse" để chọn file Excel
2. Kiểm tra các thư mục TMF
3. Click "Start Upload" để bắt đầu
4. Theo dõi tiến độ trên thanh progress
5. Xem log chi tiết trong status text

### 4.3 Xử Lý Lỗi
1. Kiểm tra status text để biết chi tiết lỗi
2. Click "Stop" để dừng khi có lỗi
3. Sửa lỗi và click "Start" để tiếp tục

## 5. Lợi Ích của GUI và Executable

### 5.1 Ưu Điểm
1. **Dễ Sử Dụng**
   - Giao diện trực quan
   - Không cần kiến thức command line
   - Hiển thị tiến độ rõ ràng

2. **Dễ Triển Khai**
   - Không cần cài đặt Python
   - Không cần cài đặt thư viện
   - Chạy được trên mọi máy Windows

3. **Dễ Bảo Trì**
   - Log chi tiết và trực quan
   - Dễ debug khi có lỗi
   - Dễ cập nhật tính năng mới

### 5.2 Lưu Ý
1. **Yêu Cầu Hệ Thống**
   - Windows 10/11
   - 4GB RAM trở lên
   - 1GB disk space

2. **Bảo Mật**
   - Mã hóa thông tin đăng nhập
   - Không lưu password
   - Tự động logout sau thời gian inactive

3. **Performance**
   - Tối ưu sử dụng RAM
   - Xử lý đa luồng cho upload
   - Cache thông minh 