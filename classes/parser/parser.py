import re

from datetime import datetime

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from classes.post.post import Post


class Parser:
    def __init__(self, root_url):
        self.__root_url = root_url

        self.row_data = set()
        self.useful_data = set()

        self.__browser = uc.Chrome(enable_cdp_events=True, options=self.set_options())

    @staticmethod
    def set_options():
        options = uc.ChromeOptions()
        options.headless = True

        return options

    def connect(self):
        self.__browser.get(self.__root_url)

    def search(self, query):
        find_field = self.__browser.find_element(By.CSS_SELECTOR, '.text-input')
        find_field.click()

        self.__browser.implicitly_wait(5)
        find_field.send_keys(query, Keys.ENTER)

        self.__browser.find_elements(By.CSS_SELECTOR, 'a.popover-option.popover-option--with-art')[-1].click()

        self.__browser.switch_to.window(self.__browser.window_handles[1])

    def select_data(self):
        print("Собираем данные...\n")

        counter = int(self.__browser.find_element(By.CSS_SELECTOR, ".v-tab--active .v-tab__counter").text)

        print(f"Найдено постов: {counter}\n")

        self.row_data.update(set(self.__browser.find_elements(By.CSS_SELECTOR, ".content-feed")))

        while len(self.row_data) < counter:
            self.__browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            search_chunk = self.__browser.find_elements(By.CSS_SELECTOR, ".search_results__chunk")[-1]
            self.row_data.update(set(search_chunk.find_elements(By.CSS_SELECTOR, '.content-feed')))

    def parse_data(self):
        print("Парсим данные...\n")

        for data in self.row_data:
            post = BeautifulSoup(data.get_attribute("innerHTML"), "lxml")

            try:
                post_title = re.sub(r"\n+Статьи редакции", "", post.find("div", class_="content-title").text.strip())
            except AttributeError:
                post_title = "---"

            post_link = post.find("a", class_="content-link").get("href")

            # Если статья выложена в подсайт
            try:
                post_author = post.find("a", class_="content-header-author__name").text.strip()
            # Если статья выложена не в подсайт
            except AttributeError:
                post_author = post.find("div", class_="content-header-author__name").text.strip()

            post_date = datetime.strptime(
                post.find("time", class_="time").get("title").replace(" (Europe/Moscow)", ''),
                '%d.%m.%Y %H:%M:%S'
            )

            try:
                post_likes_count = int(post.find(class_="like-button__count").text)
            except AttributeError:
                post_likes_count = 0

            post_comments_count = int(post.find("span", class_="comments_counter__count__value").text)

            self.useful_data.add(
                Post(post_title, post_link, post_author, post_date, post_likes_count, post_comments_count)
            )

    def execute(self):
        self.connect()

        self.search(input("Введите поисковый запрос: "))

        self.select_data()

        self.parse_data()

        self.__browser.quit()
