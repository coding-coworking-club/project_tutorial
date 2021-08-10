import logging
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class BaseballGameStatistics:

    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=os.path.abspath(path))
        self.driver.implicitly_wait(1) 
        self.base_soup = BeautifulSoup()
        self.score_soup = BeautifulSoup()
        self.inning_numbers = []
        self.inning_soups = {}
        
    def get_base_soup(self, year, kind_code, game_sno):
        self.driver.get(
            f"https://www.cpbl.com.tw/box/live?year={year}&KindCode={kind_code}&gameSno={str(game_sno)}"
        )
        self.base_soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
    def get_score_soup(self):
        self.score_soup = self.base_soup.find("div", {"class" : "tab_cont scoring active"})

    def get_inning_numbers(self):
        inning_numbers = [
            inning.get_text() 
            for inning in self.base_soup.find("div", {"class" : "InningPlaysGroup"}).\
                find("div", {"class" : "tabs"}).findAll("li")
        ]
        self.inning_numbers = inning_numbers
        for num in self.inning_numbers:
            self.inning_soups[num] = {}

    def get_play_by_play(self, inning_num):
        click_path = f"//li[a[span[contains(text(), {str(inning_num)})]]]"
        element = self.driver.find_element_by_xpath(click_path)
        element.click()
        self.inning_soups[inning_num]["play_by_play"] = BeautifulSoup(self.driver.page_source, "html.parser")

    def get_pitch_by_pitch(self, inning_num):
        click_path = f"//li[a[span[contains(text(),{str(inning_num)})]]]"
        element = self.driver.find_element_by_xpath(click_path)
        element.click()
        click_path = "//div[@class='tab_cont all_plays active']//*[contains(@class, 'batter_event') or contains(@class, 'no-pitch-action-remind')]"
        elements = self.driver.find_elements_by_xpath(click_path)
        for index, element in enumerate(elements):
            time.sleep(0.5)
            try:
                element.click()
            except:
                logging.info(f"element {index} is not clickable at point")
        self.inning_soups[inning_num]["pitch_by_pitch"] = BeautifulSoup(self.driver.page_source, "html.parser")
