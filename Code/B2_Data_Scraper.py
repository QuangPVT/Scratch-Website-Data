from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
import re
import threading
from queue import Queue
import os


# Khai báo cho dataframe 1
num_tabs = 8  # Số lượng tab Chrome tối đa cùng lúc
page_queue = Queue()  # Hàng đợi chứa URL của các trang cần cào dữ liệu


# Hàm để cào dữ liệu từ một trang
def scrape_page(main_url):
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Kích hoạt chế độ headless
    driver = webdriver.Chrome(options=chrome_options)
    width = 100
    height = 50
    driver.set_window_size(width, height)
    # Lấy dữ liệu từ URL khu vực gốc
    driver.get(main_url)
    # Chờ cho trang web tải hoàn toàn
    time.sleep(3)
    
    # Lấy dữ liệu HTML từ trang web
    html_string = driver.page_source
    soup = BeautifulSoup(html_string, 'html.parser')

    # Đóng trình duyệt
    driver.quit()

    # Cắt bớt dữ liệu không cần thiết
    target_div = soup.find('div', class_='re__pr-specs-content js__other-info')

    # Tạo một từ điển để lưu trữ cặp khoá-giá trị
    property_info_dict = {}

    # Tạo từ điển để lưu trữ cặp khoá-giá trị
    property_info = {
        'area': "N/A",
        'price': "N/A",
        'facade': "N/A",

        'entrance_wid': "N/A",
        'floors': "N/A",
        'direction_home': "N/A",
        'direction_bal': "N/A",
        'bedroom': "N/A",
        'toilet': "N/A",
        'status_doc': "N/A",
        'furniture': "N/A",
        'date_post' : "N/A",
        'date_exp' : "N/A"
    }

    # Tìm tất cả các cặp title và value và đưa vào giá trị tương ứng
    titles = soup.find_all('span', class_='re__pr-specs-content-item-title')
    values = soup.find_all('span', class_='re__pr-specs-content-item-value')
    for title, value in zip(titles, values):
        title_text = title.get_text(strip=True)
        value_text = value.get_text(strip=True)

        if "Diện tích" in title_text:
            property_info['area'] = value_text
        elif "Mức giá" in title_text:
            property_info['price'] = value_text
        elif "Mặt tiền" in title_text:
            property_info['facade'] = value_text
        elif "Đường vào" in title_text:
            property_info['entrance_wid'] = value_text
        elif "Hướng nhà" in title_text:
            property_info['direction_home'] = value_text
        elif "Hướng ban công" in title_text:
            property_info['direction_bal'] = value_text
        elif "Số tầng" in title_text:
            property_info['floors'] = value_text
        elif "Số phòng ngủ" in title_text:
            property_info['bedroom'] = value_text
        elif "Số toilet" in title_text:
            property_info['toilet'] = value_text
        elif "Pháp lý" in title_text:
            property_info['status_doc'] = value_text
        elif "Nội thất" in title_text:
            property_info['furniture'] = value_text

    # Tìm thẻ có title "Ngày đăng" và lấy giá trị từ thẻ span
    temp = soup.find("div", class_="re__pr-short-info re__pr-config js__pr-config")
    titles = temp.find_all('span', class_='title')
    values = temp.find_all('span', class_='value')
    for title, value in zip(titles, values):
        title_text = title.get_text(strip=True)
        value_text = value.get_text(strip=True)

        if "Ngày đăng" in title_text:
            property_info['date_post'] = value_text
        if "Ngày hết hạn" in title_text:
            property_info['date_exp'] = value_text
    
    # Tạo DataFrame từ dữ liệu thu thập
    df1 = pd.DataFrame([property_info])

    # Trích xuất thông tin từ mã JavaScript
    script_tags = soup.find_all('script', type='text/javascript')
    product_info = []
    
    for script_tag in script_tags:
        script_content = script_tag.string
        if script_content:
            if 'window.pageTrackingData' in script_content:
                json_data = re.search(r'JSON\.parse\(\'(.*?)\'\)', script_content)
                if json_data:
                    json_text = json_data.group(1)
                    # Phân tích chuỗi JSON
                    data = json.loads(json_text)
                    if 'products' in data:
                        products = data['products']
                        product_info.extend(products)

    # Tạo DataFrame từ dữ liệu JSON
    df2 = pd.DataFrame(product_info)

    # Kết hợp df1 và df2 thành một DataFrame duy nhất
    df_row = pd.concat([df1, df2], axis=1)

    # Thêm DataFrame này vào df_full
    global df_full
    df_full = pd.concat([df_full, df_row], ignore_index=True)
    print(len(df_full))

# Hàm để quản lý việc mở tab và cào dữ liệu
def worker():
    while True:
        url = page_queue.get()
        if url is None:
            break
        try:
            scrape_page(url)
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
        page_queue.task_done()

# Lấy danh sách tên các tệp txt trong thư mục data-hcm-links
txt_files = [f for f in os.listdir('data-hcm-links') if f.endswith('.txt')]

# Lặp qua từng tệp txt
for txt_file in txt_files:
    print(txt_file)
    # Xây dựng đường dẫn đầy đủ đến tệp txt
    txt_path = os.path.join('data-hcm-links', txt_file)

    # Đọc các liên kết từ tệp txt
    with open(txt_path, 'r') as file:
        links = file.read().splitlines()

    # Khởi tạo DataFrame df_full cho tệp csv
    df_full = pd.DataFrame()

    # Đưa các URL vào hàng đợi
    for url in links:
        page_queue.put(url)

    # Tạo danh sách các thread để cào dữ liệu
    threads = []

    for _ in range(num_tabs):
        thread = threading.Thread(target=worker)
        threads.append(thread)

    # Khởi động các thread và chờ chúng hoàn thành
    for thread in threads:
        thread.start()

    # Chờ cho tất cả các URL được xử lý
    page_queue.join()

    # Tắt các thread khi hoàn thành
    for _ in range(num_tabs):
        page_queue.put(None)

    for thread in threads:
        thread.join()

    # Lấy tên tệp csv tương ứng từ tên tệp txt
    file_name = txt_file.replace("links-", "data-")
    csv_file = os.path.splitext(file_name)[0] + '.csv'

    # Lưu DataFrame vào tệp csv
    df_full.to_csv(os.path.join('data-hcm-csv', csv_file), index=False, sep=',', encoding='utf-8')
    print(f'Done processing {file_name}')

print('All files processed')