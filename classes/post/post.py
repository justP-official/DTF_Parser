from dataclasses import dataclass
from datetime import datetime


@dataclass(unsafe_hash=True)
class Post:
    title: str
    link: str
    author: str
    publishing_date: datetime
    likes_count: int
    comments_count: int

    def __str__(self):
        return f"{self.title}, {self.link}, {self.author}, {self.publishing_date}, {self.likes_count}, {self.comments_count}"
