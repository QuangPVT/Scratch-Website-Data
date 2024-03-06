from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import threading
from queue import Queue
import os

# Khai báo các biến quan trọng
ten_quan = "thu-duc"
main_url = "https://batdongsan.com.vn/nha-dat-ban-" + ten_quan
max_page = None
href_list = []
num_tabs = 5  # Số lượng tab Chrome tối đa cùng lúc
page_queue = Queue()  # Hàng đợi chứa URL của các trang cần cào dữ liệu

# Tạo một khóa để đồng bộ việc thêm vào danh sách href
href_lock = threading.Lock()

# Hàm để cào dữ liệu từ một trang
def scrape_page(url):
    driver = webdriver.Chrome()  # Loại bỏ tùy chọn --headless để hiển thị cửa sổ trình duyệt
    
    # Thiết lập kích thước cửa sổ trình duyệt (điều chỉnh theo ý muốn)
    width = 800
    height = 600
    driver.set_window_size(width, height)

    driver.get(url)
    time.sleep(4)
    html_string = driver.page_source
    soup = BeautifulSoup(html_string, 'html.parser')
    print("Đang cào: " + url)
    with href_lock:
        # Cắt bớt dữ liệu không cần thiết
        target_div = soup.find('div', class_='re__srp-list js__srp-list')
        # Tạo danh sách các thẻ HTML chứa thông tin bất động sản
        property_tags = target_div.find_all('div', 're__card-full')
        # Bắt đầu lấy đường dẫn
        for property_tag in property_tags:
            a_tag = property_tag.find('a')
            href = a_tag['href']
            if href:
                href_list.append(main_url + href)
    
    driver.quit()

# Hàm để quản lý việc mở tab và cào dữ liệu
def worker():
    while True:
        url = page_queue.get()
        if url is None:
            break
        scrape_page(url)
        page_queue.task_done()

# Lấy dữ liệu từ URL khu vực gốc
driver = webdriver.Chrome()  # Loại bỏ tùy chọn --headless để hiển thị cửa sổ trình duyệt
driver.get(main_url)
time.sleep(3)
html_string = driver.page_source
soup = BeautifulSoup(html_string, 'html.parser')

# Kiểm tra xem URL của khu vực đó có tổng số bao nhiêu trang tối đa
pagination_numbers = soup.find_all('a', class_='re__pagination-number')
for number_tag in pagination_numbers:
    number = int(number_tag.get_text(strip=True))
    if max_page is None or number > max_page:
        max_page = number

num_page = 50
if (max_page < num_page):
    max_page = max_page
else:
    max_page = int(max_page/2)

driver.quit()

# Tạo danh sách các URL của các trang cần cào dữ liệu
page_urls = [main_url + '/p' + str(i) for i in range(1, max_page + 1)]

# Đưa các URL vào hàng đợi
for url in page_urls:
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

# Lấy đường dẫn tới thư mục chứa mã nguồn Python hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__ if '__file__' in locals() else sys.argv[0]))

# Tạo đường dẫn đầy đủ đến thư mục 'data'
data_directory = os.path.join(current_directory, 'data-hcm-links')

# Kiểm tra nếu thư mục 'data' không tồn tại thì tạo nó
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Tên file txt
file_name = 'links-' + ten_quan + '.txt'

# Đường dẫn đầy đủ đến file txt
file_path = os.path.join(data_directory, file_name)

print("Khu vực hiện có tổng số bất động sản đang bán là:",len(href_list))
with open(file_path, 'w', encoding='utf-8') as file:
    for item in href_list:
        # write each item on a new line
        file.write("%s\n" % item)
    print('Done')
