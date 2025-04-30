import logging
from datetime import datetime
import os
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class BotLogger:
    def __init__(self, excel_path, log_file='bot.log'):
        """Khởi tạo logger"""
        self.log_file = log_file
        self.excel_path = excel_path
        self.logs = []
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def _write_to_excel(self, message, level):
        """Ghi log vào sheet Logs trong Excel"""
        try:
            # Đọc sheet Logs hiện tại hoặc tạo mới nếu chưa có
            try:
                df = pd.read_excel(self.excel_path, sheet_name="Logs")
            except:
                df = pd.DataFrame(columns=["Thời gian", "Cấp độ", "Nội dung"])

            # Thêm log mới
            new_log = pd.DataFrame({
                "Thời gian": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Cấp độ": [level],
                "Nội dung": [message]
            })
            df = pd.concat([df, new_log], ignore_index=True)

            # Lưu lại vào Excel
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name="Logs", index=False)
        except Exception as e:
            print(f"Lỗi khi ghi log vào Excel: {str(e)}")

    def log(self, message):
        """Add log message to the logs list"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - INFO - {message}"
        self.logs.append(log_entry)
        logging.info(message)
        self._write_to_excel(message, "INFO")

    def log_error(self, message):
        """Log error message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - ERROR - {message}"
        self.logs.append(log_entry)
        logging.error(message)
        self._write_to_excel(message, "ERROR")

    def log_success(self, message):
        """Log success message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - SUCCESS - {message}"
        self.logs.append(log_entry)
        logging.info(message)
        self._write_to_excel(message, "SUCCESS")

    def get_logs(self):
        """Get all logs"""
        return "\n".join(self.logs)

    def clear_logs(self):
        """Clear the logs list"""
        self.logs = [] 