import re

from datetime import datetime

import requests

from fake_useragent import UserAgent

from bs4 import BeautifulSoup

from classes.post.post import Post


class Parser:
    def __init__(self, query):
        self.query = query

        self.__session = requests.Session()

        self.row_data = []
        self.useful_data = []

    @property
    def session(self):
        return self.__session

    @staticmethod
    def get_headers():
        headers = {
            "Cookie": 'pwa_disabled=always;',
            "User-agent": f'{UserAgent.random}',
            "X-Kl-Kfa-Ajax-Request": 'Ajax_Request'
        }

        return headers

    def connect(self):
        print("Подключение...")
        response = self.session.get(
            f'https://dtf.ru/search_ajax/v2/content/relevant/1?query={self.query}&mode=raw',
            headers=self.get_headers())

        return 'application/json' in response.headers.get('content-type') and response.json()['data']['counters']['entries'] > 0

    def search(self):
        if self.connect():
            print("Собираем данные...\n")

            counter = 1

            while True:
                print(f"Часть номер: {counter}")

                data = self.session.get(
                    f'https://dtf.ru/search_ajax/v2/content/relevant/{str(counter)}?query={self.query}&mode=raw',
                    headers=self.get_headers()).json()

                soup = BeautifulSoup(data['data']['feed_html'], 'lxml')

                posts = soup.findAll('div', class_="content-feed")
                self.row_data += posts

                if not data['data']['is_finished']:
                    counter += 1
                else:
                    break

            print(len(self.row_data))

    def parse_data(self):
        print("Парсим данные...\n")

        for data in self.row_data:
            # print(data.text)

            try:
                post_title = re.sub(r"\n+Статьи редакции", "",
                                    data.find("div", class_="content-title").text.strip()
                                    )
            except AttributeError:
                post_title = "---"

            post_link = data.find("a", class_="content-link").get("href")

            # Если статья выложена в подсайт
            try:
                post_author = data.find("a", class_="content-header-author__name").text.strip()
            # Если статья выложена не в подсайт
            except AttributeError:
                post_author = data.find("div", class_="content-header-author__name").text.strip()

            post_date = datetime.strptime(
                data.find("time", class_="time").get("title").replace(" (Europe/Moscow)", ''),
                '%d.%m.%Y %H:%M:%S'
            )

            post_likes_count = int(re.search(r'"count_likes":(\d+)', data.text).group(1))

            post_comments_count = int(re.search(r'"count":(\d+)', data.text).group(1))


            self.useful_data.append(
                Post(post_title, post_link, post_author, post_date, post_likes_count, post_comments_count)
            )

    def execute(self):
        self.search()

        self.parse_data()
