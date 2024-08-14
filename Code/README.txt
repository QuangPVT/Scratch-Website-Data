---

First, there must be 3 folders data-hcm-links, data-hcm-csv and data-hcm-cleaned in the same source code folder:

+ With data-hcm-links: This is the folder containing data about real estate links in a district, including paths separated by new lines (Data details read file Mo_ta_Dataset.txt)

+ With data-hcm-csv: This is the folder containing complete data about real estate after accessing batdongsan.com. The data includes basic information about real estate, prices, district codes (Data details read file Mo_ta_Dataset.txt)

+ With data-hcm-cleaned: This is the folder containing cleaned data from the data-hcm-csv folder.

Steps to scrape data on batdongsan.com with Python and Selenium library:

+ Step 1: Install the necessary libraries in the requirements.txt file with the syntax: pip install -r requirements.txt

+ Step 2: Run the following python files in turn:

- B1_Gets_Links: With this file, select the name of the district you want to scrape data to scrape the links in that district. You can fine-tune with the variable num_page which is the maximum number of pages you want to scrape, num_tabs is the number of Chrome tabs allowed to open at the same time.

- B2_Data_Scraper: With this file, the code will scrape data to get information of each link obtained after running B1_Get_Links.py. You can fine-tune with the variable num_tabs which is the number of Chrome tabs allowed to open at the same time.

- B3_Clean_Data: With this file, the code will clean the data taken from the data-hcm-csv folder to fill in the missing spaces, change the variable type, and unify the conversion to English.

---

After completing the above steps, we have 3 real estate data sets through scraping data from the website batdongsan.com
