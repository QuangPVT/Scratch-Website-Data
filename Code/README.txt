---

   Đầu tiên yêu cầu phải có 3 thư mục data-hcm-links, data-hcm-csv và data-hcm-cleaned nằm cùng thư mục mã nguồn:
   + Với data-hcm-links: Đây là thư mục chứa dữ liệu về links bất động sản trong một quận, gồm các đường dẫn được ngăn cách nhau bởi xuống dòng mới (Chi tiết dữ liệu đọc file Mo_ta_Dataset.txt)

   + Với data-hcm-csv: Đây là thư mục chứa dữ liệu đầy đủ về bất động sản sau khi được truy cập batdongsan.com. Dữ liệu gồm các thông tin cơ bản về bất động sản, giá cả, mã quận, huyện (Chi tiết dữ liệu đọc file Mo_ta_Dataset.txt)

   + Với data-hcm-cleaned: Đây là thư mục chứa dữ liệu đã làm sạch từ thư mục data-hcm-csv.

   Các bước để cào dữ liệu trên batdongsan.com với Python và bộ thư viện Selenium:
   + Bước 1: Cài đặt các thư viện cần thiết trong file requirements.txt với cú pháp: pip install -r requirements.txt

   + Bước 2: Chạy lần lượt các file python sau:
   - B1_Gets_Links: Với file này, lựa chọn tên quân bạn muốn cào dữ liệu để cào các đường dẫn trong quận đó. Có thể tinh chỉnh với biến num_page là số max trang muốn cào, num_tabs là số tab Chrome được phép mở cùng lúc.
    
   - B2_Data_Scraper: Với file này, mã sẽ cào dữ liệu để lấy thông tin của từng đường dẫn đã lấy được sau khi chạy B1_Get_Links.py. Có thể tinh chỉnh với biến num_tabs là số tab Chrome được phép mở cùng lúc.

   - B3_Clean_Data: Với file này, mã sẽ làm sạch dữ liệu được lấy từ thư mục data-hcm-csv để điền vào các chỗ bị thiếu, thay đổi loại biến, thống nhất chuyển sang tiếng anh.

---

   Sau khi hoàn thành các bước trên, ta có được 3 tập dữ liệu về bất động sản thông qua việc cào dữ liệu từ trang web batdongsan.com