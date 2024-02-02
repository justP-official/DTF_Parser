import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

from bs4 import BeautifulSoup

from classes.parser import Parser

from classes.post.post import Post

if __name__ == '__main__':
    p = Parser("https://dtf.ru/")
    p.execute()

    for post in p.useful_data:
        print(post)
