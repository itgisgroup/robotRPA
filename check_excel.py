import pandas as pd

# Đọc file Excel
excel_path = "Update_DescriptionDrawer.xlsx"
try:
    print(f"\nĐang đọc file Excel: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name="Danh sách file cần upload")
    
    print("\nTổng số dòng trong Excel:", len(df))
    
    print("\nCác cột trong Excel:")
    print(df.columns.tolist())
    
    print("\nMẫu dữ liệu:")
    print(df.head())
    
    print("\nThống kê trạng thái:")
    print(df["Trạng thái"].value_counts())
    
    print("\nKiểm tra các dòng có trạng thái trống:")
    empty_status = df["Trạng thái"].isna()
    print("Số dòng trạng thái trống:", empty_status.sum())
    
    if empty_status.sum() > 0:
        print("\nCác dòng có trạng thái trống:")
        print(df[empty_status])
        
except Exception as e:
    print(f"Lỗi khi đọc file Excel: {str(e)}") 