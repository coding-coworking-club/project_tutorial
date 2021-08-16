import os
import sys
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class AbsInterface:
	def __init__(self, classname=None):
		self.process = classname
	
	def run(self):
		self.process().run()

# class Scraper(ABC):

# 	def set_option(self):
# 		options = Options()
# 		options.add_argument("--disable-notifications")

#     def set_chromedriver(self):
#         current_directory = self.file_path()
#         chromedriver_path = os.path.join(current_directory, "resource/chromedriver")
#         driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
# 		driver.implicitly_wait(10) # seconds
    
#     def file_path(self):
#         file_path = os.path.abspath(os.getcwd())
#         return file_path

# 	def run(self):
# 		pass
class Scraper:


    def __init__(self):

        self.options = self._set_options()
        self.driver = self._set_driver

        file_path = os.path.abspath(os.getcwd())
        chromedriver_path = os.path.join(file_path, "resource/chromedriver")

    def _set_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--headless")

    def _set_driver(self):
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=self.options)

    def get_header(cls):
        cls.title = cls.driver.get(cls.home)
        return cls.title
    
    def scroll_down(self):
        for times in range(1, 10):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(1)
            print(f"scroll down {times} times")
    
    def get_all_item_page(self):
        pass

    def get_item_list(self):
        pass

    def get_item_list(self):
        pass

    def get_item_name(self):
        pass

    def get_item_picture(self):
        pass


    def get_item_color(self):
        pass

    def get_item_size(self):
        pass


class MIU(Scraper):

    def __init__(self, home_url) -> None:
        self.home = home_url
        super().__init__()

    def get_all_item_page(self):
        search_input = self.driver.find_element_by_class_name("nav-menu-link")
        print("first text", search_input.text)
        print(f"click {search_input.text}")
        search_input.click()
        search_input = self.driver.find_element_by_class_name("icon-slim-arrow-down")
        print(f"click {search_input.text}")
        search_input.click()
        search_input = self.driver.find_element_by_class_name("category-level1")
        search_input = self.driver.find_element_by_class_name("category-menu-item-link")
        print("second text", search_input.text)
        print(f"click {search_input.text}")
        search_input.click()

    def get_item_list(self):
        pass

    def get_item_list(self):
        pass

    def get_item_name(self):
        pass

    def get_item_picture(self):
        pass

    def get_item_color(self):
        pass

    def get_item_size(self):
        pass

home = "https://www.miu-star.com.tw/"
scrpaer_miu = MIU(home)
title = scrpaer_miu.get_header()
print(title)
scrpaer_miu.get_all_item_page()
scrpaer_miu.scroll_down()


# ProductA = Scraper()

# create_product_a = AbsInterface()
# create_product_a.process = ProductA
# create_product_a.run()
