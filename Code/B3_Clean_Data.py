import pandas as pd
from datetime import datetime
import pandas as pd
import os
import shutil

# Đường dẫn thư mục chứa các file CSV gốc
input_folder = 'data-hcm-csv/Dataset_Sample'

# Đường dẫn thư mục chứa các file CSV đã làm sạch
output_folder = 'data-hcm-cleaned/Dataset_Sample'

# Kiểm tra nếu thư mục output chưa tồn tại, tạo mới nếu cần
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lặp qua các file trong thư mục input
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        # Tạo đường dẫn đầy đủ cho file đầu vào
        input_file_path = os.path.join(input_folder, file_name)

        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(input_file_path)

        # Thực hiện các bước làm sạch như trong đoạn mã của bạn
        # 1. Chuẩn hóa cột 'area'
        df['area'] = df['area'].str.replace(' m²', '')
        df['area'] = df['area'].str.replace('.', '')
        df['area'] = df['area'].str.replace(',', '.').astype(float)

        # 2. Chuẩn hóa cột 'price' 
        # Cần sửa code, sai hệ số tỷ
        # Cần kiểm tra xem là có 'triệu/m²', nếu có thì lấy số price_num * area = price
        # 'Thỏa thuận' thì biến thành N/A
        df['price'] = df['price'].str.replace('.', '')
        df['price'] = df['price'].str.replace(',', '.')

        def process_price(row):
            if 'triệu/m' in row['price']:
                # Kiểm tra và xử lý 'triệu/m²'
                return pd.to_numeric(row['price'][:-8]) * row['area']
            elif 'Thỏa' in row['price']:
                # Xử lý 'thỏa thuận'
                return None
            else:
                # Chuyển đổi về định dạng số
                row['price'] = row['price'].replace(' triệu', '')
                row['price'] = row['price'].replace(' tỷ', 'e3')
                return pd.to_numeric(row['price'], errors='coerce')

        # Áp dụng hàm process_price cho cột 'price'
        df['price'] = df.apply(process_price, axis=1)

        # Chuyển đổi về định dạng số (nếu cần)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # 3. Chuẩn hóa cột 'facade', 'entrance_wid'
        df['facade'] = df['facade'].str.replace(',', '.')
        df['facade'] = df['facade'].str.replace(' m', '').astype(float)
        df['entrance_wid'] = df['entrance_wid'].str.replace(',', '.')
        df['entrance_wid'] = df['entrance_wid'].str.replace(' m', '').astype(float)

        # 4. status_doc, furniture cho thành true / false
        df['status_doc'] = df['status_doc'].apply(lambda x: "True" if x == "N/A" else "False")
        df['furniture'] = df['furniture'].apply(lambda x: "True" if x == "N/A" else "False")

        # 5. bedroom và toilet
        df['bedroom'] = df['bedroom'].str.replace(' phòng', '').astype(float)
        df['toilet'] = df['toilet'].str.replace(' phòng', '').astype(float)

        # 6. Chuẩn hóa cột 'date_post' và 'date_exp'
        df['date_post'] = pd.to_datetime(df['date_post'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        df['date_exp'] = pd.to_datetime(df['date_exp'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

        # 7. Chuẩn hóa cột 'floors'
        df['floors'] = pd.to_numeric(df['floors'], errors='coerce')

        # 8. Chuẩn hóa cột 'direction_home' và 'direction_bal'
        df['direction_home'] = df['direction_home'].str.lower()
        df['direction_bal'] = df['direction_bal'].str.lower()
        # Tạo bảng ánh xạ từ tiếng Việt sang tiếng Anh và viết tắt
        direction_mapping = {
            'đông': 'east', 'tây': 'west',
            'nam': 'south', 'bắc': 'north',
            # Thêm các giá trị khác nếu cần
        }

        # Thay thế giá trị trong cột 'direction_home'
        df['direction_home'] = df['direction_home'].map(direction_mapping)

        # Thay thế giá trị trong cột 'direction_bal'
        df['direction_bal'] = df['direction_bal'].map(direction_mapping)

        # 6. Chuẩn hóa cột 'intent' và 'pageType'
        df['intent'] = df['intent'].str.lower()
        df['pageType'] = df['pageType'].str.lower()

        # Lưu dữ liệu đã làm sạch vào một tệp CSV trong thư mục output
        output_file_name = 'cleaned-' + file_name
        output_file_path = os.path.join(output_folder, output_file_name)
        df.to_csv(output_file_path, sep=',', index=False)

        print(f"Done cleaning and saving: {output_file_path}")

print("All files processed.")


