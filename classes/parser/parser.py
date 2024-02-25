import re

from datetime import datetime

import requests

from fake_useragent import UserAgent

from bs4 import BeautifulSoup

from classes.post.post import Post

from classes.question.question import Question
from classes.question.bool_question import BoolQuestion


class Parser:
    """
    Класс для парсинга сайта 'dtf.ru'.

    ...

    Атрибуты:
    ---------
    prompt : str
        Поисковый запрос.
    __session : Session
        Объект класса Session. Используется для подключения к сайту.
    filters : dict
        Словарь с фильтрами для расширенного поиска.
    useful_data : list
        Список, в котором хранятся собранные данные.

    Методы:
    -------
    set_headers
        Статичный метод. Возвращает словарь для настройки заголовков атрибута session.
    set_filters
        Статичный метод. Возвращает словарь для настройки расширенного поиска атрибута filters.
    build_query(page_number)
        Возвращает строку с параметрами поиска.
    connect(response)
        Статичный метод. Проверяет, прислал ли сервер JSON. Возвращает булево значение.
    search
        Подключается к серверу, ищет нужные данные и передаёт их в метод parse_data. Возвращает None.
    parse_data(raw_data)
        Парсит полученные данные. Затем добавляет их в useful_data. Возвращает None.
    """

    def __init__(self, prompt: str):
        """
        Инициализация экземпляра класса Parser.

        Параметры
        ---------
        prompt : str
            Поисковый запрос.

        Атрибуты
        --------
        __session : Session
            Приватный атрибут. Объект класса Session. Используется для подключения к сайту.
        filters : dict
            Словарь с фильтрами для расширенного поиска.
        useful_data : list
            Список, в котором хранятся собранные данные.
        """
        self.prompt = prompt

        self.__session = requests.Session()
        self.session.headers.update(self.set_headers())

        self.filters = self.set_filters()

        self.useful_data = []

    @property
    def session(self):
        return self.__session

    @staticmethod
    def set_headers() -> dict:
        """
        Статичный метод. Используется для настройки заголовков запроса к серверу.

        Возвращаемое значение
        ---------------------
        headers : dict
            Словарь с заголовками запроса.
        """

        headers = {
            "Cookie": 'pwa_disabled=always;',
            "User-agent": f'{UserAgent.chrome}',
            "accept": 'application/json',
            "X-Kl-Kfa-Ajax-Request": 'Ajax_Request'
        }

        return headers

    @staticmethod
    def set_filters() -> dict:
        """
        Статичный метод. Используется для настройки расширенного поиска.

        Для функционала использует классы Question и BoolQuestion.

        Возвращаемое значение
        ---------------------
        search_filters : dict
            Словарь с фильтрами для расширенного поиска
        """
        search_filters = {
            'sort_type': 'relevant',  # если по релевантности, то "relevant" иначе "new"
            'strict': '',             # если Точное совпадение, то '&strict=1', иначе ''
            'title': '',              # если По заголовкам, то '&title=1', иначе ''
            'editorial': '',          # если Материал редакции, то '&editorial=1', иначе ''
            'blog': '',               # если Личный блог, то '&blog=1', иначе ''
        }

        is_advanced_search = BoolQuestion(
            'Использовать расширенный поиск?\n1. Да;\n2. Нет;',
            'is_advanced')

        if is_advanced_search:
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

    def build_query(self, page_number: int) -> str:
        """
        Формирует поисковый запрос.

        Параметры
        ---------
        page_number : int
            Номер страницы поиска

        Возвращаемое значение
        ---------------------
        query : str
            Строка с поисковым запросом
        """
        query = f'{self.filters["sort_type"]}/{str(page_number)}?query={self.prompt}{self.filters["strict"]}{self.filters["title"]}{self.filters["editorial"]}{self.filters["blog"]}&mode=raw'

        return query

    @staticmethod
    def connect(response: requests.Response) -> bool:
        """
        Статичный метод. Проверяет, прислал ли сервер JSON.

        Параметры
        ---------
        response : requests.Response
            Экземпляр класса Response.

        Возвращаемое значение
        ---------------------
        bool: True, если сервер прислал JSON, иначе False.
        """
        print("Подключение...\n")

        return 'application/json' in response.headers.get('content-type')

    def search(self) -> None:
        """
        Ищет данные с учётом заданных фильтров.

        Создаётся бесконечный цикл, так как заранее неизвестно сколько существует подходящих записей.

        С помощью метода build_query формируется поисковый запрос.

        Затем, при помощи атрибута __session идёт запрос к серверу.

        Если сервер не прислал JSON, то выходим из цикла и завершаем работу программы,
        иначе продолжаем работу.

        Из полученного JSON извлекается поле 'feed_html', в котором хранятся нужные данные.

        Из html-разметки ищутся записи, которые содержат CSS-классы 'content-feed'.

        Полученный список отправляется в метод parse_data, где происходит дальнейший парсинг.

        В конце идёт проверка, закончились ли записи. Если нет, то цикл продолжается.

        Возвращаемое значение
        ---------------------
        None
        """

        print("Собираем данные...\n")

        counter = 1

        while True:
            url = f"https://dtf.ru/search_ajax/v2/content/{self.build_query(counter)}"

            response = self.session.get(url)

            if counter == 1:
                if not self.connect(response):
                    break

            data = response.json()

            if data['data']['counters']['entries'] == 0:
                print("Ничего не найдено...\n")
                break

            print(f"Часть номер: {counter}")

            soup = BeautifulSoup(data['data']['feed_html'], 'lxml')

            posts = soup.findAll('div', class_="content-feed")
            self.parse_data(posts)

            if not data['data']['is_finished']:
                counter += 1
            else:
                break

    def parse_data(self, row_data: list) -> None:
        """
        Парсит данные из списка row_data.

        Ищет следующие данные:
            1. Заголовок;
            2. Ссылка;
            3. Имя автора;
            4. Дата публикации;
            5. Количество лайков;
            6. Количество комментариев;

        Потом объединяет полученные данные в экземпляр класс Post и добавляет его в список useful_data.

        Параметры
        ---------
        row_data : list
            Список с необработанными данными.

        Возвращаемое значение
        ---------------------
        None
        """
        if len(row_data) > 0:
            print("Парсим данные...\n")

        for data in row_data:
            # Получаем заголовок статьи. Если он есть, то убираем лишние символы и плашку "Статьи редакции"
            try:
                post_title = re.sub(r"\n+Статьи редакции", "",
                                    data.find("div", class_="content-title").text.strip()
                                    )
            # Иначе, если заголовка нет, ставим прочерк
            except AttributeError:
                post_title = "---"

            # Получаем ссылку на статью
            post_link = data.find("a", class_="content-link").get("href")

            # Получаем имя автора статьи. Если статья выложена в подсайт
            try:
                post_author = data.find("a", class_="content-header-author__name").text.strip()
            # Если статья выложена не в подсайт
            except AttributeError:
                post_author = data.find("div", class_="content-header-author__name").text.strip()

            # Получаем дату публикации статьи
            post_date = datetime.strptime(
                data.find("time", class_="time").get("title").replace(" (Europe/Moscow)", ''),
                '%d.%m.%Y %H:%M:%S'
            )

            # Получаем количество лайков статьи, если они есть
            try:
                post_likes_count = int(re.search(r'"count_likes":(\d+)', data.text).group(1))
            # Иначе, если лайков нет, ставим 0
            except AttributeError:
                post_likes_count = 0

            # Получаем количество комментариев статьи, если они есть
            try:
                post_comments_count = int(re.search(r'"count":(\d+)', data.text).group(1))
            # Иначе, если комментариев нет, ставим 0
            except AttributeError:
                post_comments_count = 0

            # Сохраняем полученные данные в список useful_data
            self.useful_data.append(
                Post(post_title, post_link, post_author, post_date, post_likes_count, post_comments_count)
            )
