import os
import re
import time

import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def first_query_page(crime, place, path):
    # access the main page of "Law and Regulations Retrieving System"
    driver = webdriver.Chrome(executable_path=os.path.abspath(path))
    url = "https://law.judicial.gov.tw/FJUD/default_AD.aspx"
    driver.get(url)

    # find element and simulate the click
    driver.find_element_by_name("jud_sys").click()
    content = driver.find_element_by_name("jud_kw")
    content.send_keys(crime)
    driver.find_element_by_name("ctl00$cp_content$btnQry").click()
    court = driver.find_element_by_partial_link_text(place)
    actions = ActionChains(driver).move_to_element(court).key_down(Keys.CONTROL).key_down(
        Keys.SHIFT).click(court).key_up(Keys.CONTROL).key_up(Keys.SHIFT)
    actions.perform()

    # retrieve page of query result
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    time.sleep(0.5)

    # switch to the page
    page_url = driver.current_url
    return page_url


def get_bs4_content(url):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_main_text(content):
    raw_text = content.find("body").find(
        "div", {"class": "text-pre text-pre-in"})
    sentences = raw_text.find_all(
        text=lambda text: isinstance(text, Comment))
    main_text = ",".join(sentences)
    return main_text


def get_full_text(content):
    nodes = content.find("body").find_all("td")
    full_text = ",".join([node.text for node in nodes])
    return full_text
