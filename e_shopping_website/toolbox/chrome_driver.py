import errno
import os
import re
import sys
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MacOSChromeDriver:
    def _get_os_chromedriver_version(self):
        chrome_path = "/Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions"
        if os.path.isdir(chrome_path):
            ls = os.listdir(chrome_path)
            for directory in ls:
                version = re.match(r"\d*", directory)
                if version:
                    print(f"Chrome driver {directory}")
                    return version.group()
            raise FileNotFoundError("no file match r'\d*' rule")
        raise FileNotFoundError(chrome_path)

    def get_chromedriver_path(self):
        version = self._get_os_chromedriver_version()
        chromedriver = f"./resource/mac-64-m1-{version}/chromedriver"
        return chromedriver
