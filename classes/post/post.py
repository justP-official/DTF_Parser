from dataclasses import dataclass
from datetime import datetime


@dataclass(unsafe_hash=True)
class Post:
    """
    Класс для хранения данных из статьи.

    Атрибуты
    --------
    title : str
        Заголовок статьи.
    link : str
        Ссылка на статью.
    author : str
        Автор статьи.
    publishing_date : datetime
        Дата публикации статьи.
    likes_count : int
        Количество лайков статьи.
    comments_count : int
        Количество комментариев статьи.
    """
    title: str
    link: str
    author: str
    publishing_date: datetime
    likes_count: int
    comments_count: int

    def __str__(self):
        return f"{self.title};{self.link};{self.author};{self.publishing_date};{self.likes_count};{self.comments_count}"

    def __iter__(self):
        return iter(str(self).split(";"))

    def __next__(self):
        return next(self)
