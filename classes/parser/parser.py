import re

from datetime import datetime

import requests

from fake_useragent import UserAgent

from bs4 import BeautifulSoup

from classes.post.post import Post

from classes.question.question import Question


class Parser:
    def __init__(self, prompt):
        self.prompt = prompt

        self.__session = requests.Session()

        self.filters = self.set_filters()

        self.row_data = []
        self.useful_data = []

    @property
    def session(self):
        return self.__session

    @staticmethod
    def get_headers():
        headers = {
            "Cookie": 'pwa_disabled=always;',
            "User-agent": f'{UserAgent.chrome}',
            'accept': 'application/json',
            "X-Kl-Kfa-Ajax-Request": 'Ajax_Request'
        }

        return headers

    @staticmethod
    def set_filters():
        search_filters = {
            'sort_type': 'relevant',  # если по релевантности, то "relevant" иначе "new"
            'strict': '',             # если Точное совпадение, то '&strict=1', иначе ''
            'title': '',              # если По заголовкам, то '&title=1', иначе ''
            'editorial': '',          # если Материал редакции, то '&editorial=1', иначе ''
            'blog': '',               # если Личный блог, то '&blog=1', иначе ''
        }

        is_advanced_search = Question(
            'Использовать расширенный поиск?\n1. Да;\n2. Нет;',
            'is_advanced',
            (True, False)).give_response()

        if is_advanced_search['is_advanced']:
            questions = (
                Question(
                    'Как сортировать записи?\n1. По релевантности;\n2. По дате;',
                    'sort_type',
                    ('relevant', 'new')
                ),
                Question(
                    'Точное совпадение\n1. Да;\n2. Нет;',
                    'strict',
                    ('&strict=1', '')
                ),
                Question(
                    'По заголовкам\n1. Да;\n2. Нет;',
                    'title',
                    ('&title=1', '')
                ),
                Question(
                    'Материал редакции\n1. Да;\n2. Нет;',
                    'editorial',
                    ('&editorial=1', '')
                ),
                Question(
                    'Личный блог\n1. Да;\n2. Нет;',
                    'blog',
                    ('&blog=1', '')
                ),
            )

            for question in questions:
                response = question.give_response()

                search_filters.update(response)

        return search_filters

    def build_query(self, page_number):
        query = f'{self.filters["sort_type"]}/{str(page_number)}?query={self.prompt}{self.filters["strict"]}{self.filters["title"]}{self.filters["editorial"]}{self.filters["blog"]}&mode=raw'

        return query

    @staticmethod
    def connect(response):
        print("Подключение...")

        return 'application/json' in response.headers.get('content-type')

    def search(self):

        print("Собираем данные...\n")

        counter = 1

        while True:
            url = f"https://dtf.ru/search_ajax/v2/content/{self.build_query(counter)}"

            response = self.session.get(url, headers=self.get_headers())

            if counter == 1:
                if not self.connect(response):
                    break

            print(f"Часть номер: {counter}")

            data = response.json()

            soup = BeautifulSoup(data['data']['feed_html'], 'lxml')

            posts = soup.findAll('div', class_="content-feed")
            self.row_data += posts

            if not data['data']['is_finished']:
                counter += 1
            else:
                break

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
