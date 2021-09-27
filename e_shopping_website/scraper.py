import logging
import re
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from clothes.models import Website
from config.system_setting import ScraperConfig
from toolbox.chrome_driver import MacOSChromeDriver

logger = logging.getLogger(__name__)
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"

import django

django.setup()


class AbsInterface:
    def __init__(self, classname=None):
        self.process = classname

    def run(self):
        self.process().run()


class Scraper:

    need_scroll_down = False

    def __init__(self):
        self._set_options()
        self.driver = self._set_driver()

    def _set_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        # self.options.add_argument("--headless")

    def _set_driver(self):
        chromedriver_path = MacOSChromeDriver().get_chromedriver_path()
        driver = webdriver.Chrome(
            executable_path=chromedriver_path, options=self.options
        )
        return driver

    def _get_home(self):
        self.driver.get(self.home)

    def get_header(self):
        return self.driver.title

    def _scroll_down(self):
        need_scroll_down, times = self.config.get("NEED_SCROLL_DOWN")
        if need_scroll_down:
            for count in range(1, times):
                self.driver.execute_script(
                    "window.scrollTo(0,document.body.scrollHeight)"
                )
                sleep(1)
                print(f"scroll down {count} times")

    def _get_all_item_page(self):
        pass

    def _get_item_list(self):
        pass

    def _git_item_info(self):
        pass

    def get_item_name(self):
        pass

    def get_item_picture(self):
        pass

    def get_item_color(self):
        pass

    def get_item_size(self):
        pass


class MIUSTAR(Scraper):
    def __init__(self):
        super().__init__()

        self.config = ScraperConfig(
            f"./config/config-{__class__.__name__.lower()}.json"
        )
        self.home = self.config["HOME_PAGE"]
        self._get_home()
        self._get_all_item_page()
        self._scroll_down()
        self._get_item_list()
        self._get_item_info()

    def _get_home(self):
        print(f"start to get home: {self.home}")
        self.driver.get(self.home)
        close_button = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        print("click close button")
        close_button.click()
        contract = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[8]/a'))
        )
        print(f"click {contract.text}")
        contract.click()

    def _get_all_item_page(self):
        search_input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        print("first text", search_input.text)
        print(f"click {search_input.text}")
        search_input.click()
        search_input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon-slim-arrow-down"))
        )
        # search_input = self.driver.find_element_by_class_name("")
        search_input.click()
        search_input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "category-level1"))
        )
        search_input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "category-menu-item-link"))
        )
        print("second text", search_input.text)
        print(f"click {search_input.text}")
        search_input.click()
        sleep(1)

    def _get_item_list(self):
        # 把本頁搜尋商品的網址截下來
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        item_list = soup.find_all("li", {"class": "column-grid-container__column"})
        self.item_list_path = []
        for item in item_list:
            self.item_list_path.append(item.a["href"])
        print(self.item_list_path)

    def _get_item_info(self):
        # 新的分頁
        for path in self.item_list_path:
            url = f"{self.config['HOME_PAGE']}{path}"
            self.driver.get(url)
            print(url)
            picture = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, "large-image-frame"))
            )
            # 爬詳細的圖文
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            picture = soup.find("figure", {"class": "large-image-frame"}).img["src"]
            picture_url = f"https:{picture}"
            print(picture_url)

            name = soup.find("h1", {"class": "salepage-title"}).text.strip()
            try:
                name = name.split("★")[2].split("(")[0]
                print(name)
            except:
                name = name.split("★")[1].split("(")[0]
                print(name)

            price = soup.find(
                "div", {"class": "salepage-price cms-moneyColor"}
            ).text.strip()
            print(price)

            color_size = soup.find("ul", {"class": "sku-ul"})
            color_size_all = color_size.find_all("a")
            color_size_list = [color_size.text for color_size in color_size_all]
            print(color_size_list)
            chinese = r"[\u4e00-\u9fff]+"
            color_list = [
                re.findall(chinese, color_size) for color_size in color_size_list
            ]
            color_list = list({color[0] for color in color_list if color})
            print(color_list)
            number_eng = r"[a-zA-Z]+\'*[a-z]*|[0-9.]*[0-9]+[a-zA-Z]+\'*[a-z]*"
            size_list = [
                re.findall(number_eng, color_size) for color_size in color_size_list
            ]
            size_list = list({size[0] for size in size_list if size})
            print(size_list)

    # def get_item_name(self):
    #     pass

    # def get_item_picture(self):
    #     pass

    # def get_item_color(self):
    #     pass

    # def get_item_size(self):
    #     pass


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
    miustart_scraper = MIUSTAR()
