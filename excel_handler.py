import pandas as pd
import os
import shutil
from datetime import datetime

class ExcelHandler:
    def __init__(self, excel_path):
        """Khởi tạo Excel handler"""
        self.excel_path = excel_path
        self.main_sheet = "Danh sách file cần upload"
        self.completed_sheet = "Upload Hoàn thành"
        self.log_sheet = "Log"
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Không tìm thấy file Excel tại: {excel_path}")
            
        # Tạo sheet Log nếu chưa tồn tại
        try:
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a') as writer:
                if self.log_sheet not in pd.ExcelFile(self.excel_path).sheet_names:
                    log_df = pd.DataFrame(columns=["Thời gian", "Tên file", "Hành động", "Trạng thái", "Người thực hiện"])
                    log_df.to_excel(writer, sheet_name=self.log_sheet, index=False)
        except Exception as e:
            print(f"Lỗi khi tạo sheet Log: {str(e)}")
            
    def initialize_status(self):
        """Khởi tạo trạng thái 'Chờ xử lý' cho các file chưa có trạng thái"""
        try:
            print("Đang khởi tạo trạng thái cho các file...")
            
            # Đọc sheet chính
            df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
            
            # Đếm số file chưa có trạng thái
            empty_status = df["Trạng thái"].isna()
            count = empty_status.sum()
            print(f"Số file chưa có trạng thái: {count}")
            
            if count > 0:
                # Cập nhật trạng thái
                df.loc[empty_status, "Trạng thái"] = "Chờ xử lý"
                
                # Lưu lại vào Excel
                with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=self.main_sheet, index=False)
                    
                print("Đã cập nhật trạng thái cho các file")
            else:
                print("Không có file nào cần khởi tạo trạng thái")
                
        except Exception as e:
            print(f"Lỗi khi khởi tạo trạng thái: {str(e)}")
            
    def read_pending_files(self):
        """Đọc danh sách file chờ xử lý"""
        try:
            print("\nĐang đọc danh sách file chờ xử lý...")
            df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
            
            # In ra để debug
            print("\nTất cả các trạng thái hiện có:")
            print(df["Trạng thái"].unique())
            
            # Chuẩn hóa trạng thái
            df["Trạng thái"] = df["Trạng thái"].astype(str).str.strip()
            
            # In ra sau khi chuẩn hóa
            print("\nCác trạng thái sau khi chuẩn hóa:")
            print(df["Trạng thái"].unique())
            
            # Lọc các file chờ xử lý
            pending_mask = df["Trạng thái"] == "Chờ xử lý"
            pending_files = df[pending_mask].to_dict('records')
            
            print(f"\nTìm thấy {len(pending_files)} file cần xử lý")
            if len(pending_files) > 0:
                print("Danh sách file cần xử lý:")
                for file in pending_files:
                    print(f"- {file['Tên file (File name)']} - Trạng thái: {file['Trạng thái']}")
            
            return pending_files
        except Exception as e:
            print(f"Lỗi khi đọc danh sách file chờ xử lý: {str(e)}")
            return []
        
    def read_uploaded_files(self):
        """Đọc danh sách file đã upload thành công"""
        df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
        return df[df["Trạng thái"] == "Đã upload thành công"].to_dict('records')
        
    def add_log(self, file_name, action, status):
        """Thêm log vào sheet Log"""
        try:
            # Đọc sheet Log
            try:
                log_df = pd.read_excel(self.excel_path, sheet_name=self.log_sheet)
            except:
                log_df = pd.DataFrame(columns=["Thời gian", "Tên file", "Hành động", "Trạng thái", "Người thực hiện"])
            
            # Thêm log mới
            new_log = {
                "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Tên file": file_name,
                "Hành động": action,
                "Trạng thái": status,
                "Người thực hiện": "Bot"
            }
            log_df = pd.concat([log_df, pd.DataFrame([new_log])], ignore_index=True)
            
            # Lưu lại sheet Log
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                log_df.to_excel(writer, sheet_name=self.log_sheet, index=False)
                
        except Exception as e:
            print(f"Lỗi khi thêm log: {str(e)}")
            
    def update_status(self, file_name, status):
        """Cập nhật trạng thái cho file"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
            mask = df["Tên file (File name)"] == file_name
            if mask.any():
                df.loc[mask, "Trạng thái"] = status
                with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=self.main_sheet, index=False)
                
                # Thêm log
                self.add_log(file_name, "Cập nhật trạng thái", status)
                
        except Exception as e:
            print(f"Lỗi khi cập nhật trạng thái: {str(e)}")
            
    def update_drawing_id(self, file_name, drawing_id):
        """Cập nhật Drawing ID cho file"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
            mask = df["Tên file (File name)"] == file_name
            if mask.any():
                df.loc[mask, "ID file (CADDi)"] = drawing_id
                with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=self.main_sheet, index=False)
                    
                # Thêm log
                self.add_log(file_name, "Cập nhật Drawing ID", drawing_id)
                
        except Exception as e:
            print(f"Lỗi khi cập nhật Drawing ID: {str(e)}")
            
    def move_to_completed(self, file_name):
        """Di chuyển dòng sang sheet hoàn thành"""
        try:
            # Đọc cả hai sheet
            main_df = pd.read_excel(self.excel_path, sheet_name=self.main_sheet)
            try:
                completed_df = pd.read_excel(self.excel_path, sheet_name=self.completed_sheet)
            except:
                completed_df = pd.DataFrame(columns=main_df.columns)
            
            # Tìm dòng cần di chuyển
            mask = main_df["Tên file (File name)"] == file_name
            if mask.any():
                # Lấy dòng cần di chuyển
                row_to_move = main_df[mask]
                
                # Thêm vào sheet hoàn thành
                completed_df = pd.concat([completed_df, row_to_move], ignore_index=True)
                
                # Xóa khỏi sheet chính
                main_df = main_df[~mask]
                
                # Lưu lại cả hai sheet
                with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    main_df.to_excel(writer, sheet_name=self.main_sheet, index=False)
                    completed_df.to_excel(writer, sheet_name=self.completed_sheet, index=False)
                    
                # Thêm log
                self.add_log(file_name, "Di chuyển sang sheet hoàn thành", "Hoàn thành")
                    
        except Exception as e:
            print(f"Lỗi khi di chuyển dòng sang sheet hoàn thành: {str(e)}")
            
    def move_file(self, file_name, source_dir, dest_dir):
        """Di chuyển file giữa các thư mục"""
        try:
            source_path = os.path.join(source_dir, file_name)
            dest_path = os.path.join(dest_dir, file_name)
            if os.path.exists(source_path):
                shutil.move(source_path, dest_path)
                print(f"Đã di chuyển file {file_name} từ {source_dir} sang {dest_dir}")
            else:
                print(f"Không tìm thấy file {file_name} trong thư mục {source_dir}")
        except Exception as e:
            print(f"Lỗi khi di chuyển file: {str(e)}") 