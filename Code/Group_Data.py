import os
import pandas as pd

# Lấy đường dẫn của thư mục chứa file code
current_directory = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn đến thư mục chứa các file CSV (nằm cùng với file code)
folder_path = os.path.join(current_directory, 'data-hcm-links/Dataset_Sample')

# Danh sách các file trong thư mục
files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Khởi tạo DataFrame rỗng để lưu dữ liệu gom lại
combined_data = pd.DataFrame()

# Đọc từng file và gom lại vào DataFrame
for file in files:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    combined_data = pd.concat([combined_data, data], ignore_index=True)

# Lưu DataFrame gom lại thành một file CSV lớn
output_file_path = os.path.join(current_directory, 'all_data_hcm_links.csv')
combined_data.to_csv(output_file_path, index=False)

print(f'Gom dữ liệu thành công. File {output_file_path} đã được tạo.')
