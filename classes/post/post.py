class Post:
    def __init__(self, title, link, author, publishing_date, likes_count, comments_count):
        self.title = title
        self.link = link
        self.author = author
        self.publishing_date = publishing_date
        self.likes_count = likes_count
        self.comments_count = comments_count

    def __str__(self):
        return f"{self.title}, {self.link}, {self.author}, {self.publishing_date}, {self.likes_count}, {self.comments_count}"
