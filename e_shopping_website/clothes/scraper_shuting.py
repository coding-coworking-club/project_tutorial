import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseballGameStatistics:

    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=os.path.abspath(path))
        self.inning_numbers = []
        self.base_soup = BeautifulSoup()
        self.inning_soups = {}
        
    def game_request(self, year, kind_code, game_sno):
        self.driver.get(f"https://www.cpbl.com.tw/box/live?year={year}&KindCode={kind_code}&gameSno={str(game_sno)}")
        self.base_soup = BeautifulSoup(self.driver.page_source, "html.parser")

    def get_inning_numbers(self):
        inning_numbers = [
            inning.get_text() 
            for inning in self.base_soup.find("div", {"class" : "InningPlaysGroup"}).\
                find("div", {"class" : "tabs"}).findAll("li")
        ]
        self.inning_numbers = inning_numbers

    def click_inning(self, inning_num):
        click_path = \
            f"/html/body/div[2]/div[1]/div/form/div[4]/div[2]/div[2]/div[2]/div/div[1]/ul/li[{str(inning_num)}]/a/span"
        self.driver.find_element_by_xpath(click_path).click()
        self.inning_soups[inning_num] = {"all": BeautifulSoup(self.driver.page_source, "html.parser")}

    def all_plays_half_inning_parser(self, inning_num, half_inning):
        half_inning_soup = self.inning_soups[inning_num]["all"].find("div", {"class" : "tab_cont all_plays active"}).\
            find("div",{"class" : "InningPlaysGroup"}).\
                find("section", {"class" : half_inning}).\
                    findAll("div",{"class","item play"})
        self.inning_soups[inning_num][half_inning] = {"soup_list": half_inning_soup}

    def get_player_names(self, inning_num, half_inning):
        player_names = [soup.find("div", {"class" : "info"}).\
            find("div", {"class" : "desc"}).find("a").get_text() 
            for soup in self.inning_soups[inning_num][half_inning]["soup_list"]
        ]
        self.inning_soups[inning_num][half_inning]["player_names"] = player_names
