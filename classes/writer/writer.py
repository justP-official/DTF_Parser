import csv

from classes.question.question import Question
from classes.question.prompt_question import PromptQuestion


class Writer:
    def __init__(self, data):
        self.data = data

        self.filename = 'output.csv'

    def change_filename(self):
        new_filename = PromptQuestion(
            f'Изменить имя файла по умолчанию? (По умолчанию: {self.filename})\n1. Да;\n2. Нет;',
            'is_rename'
        ).give_prompt()

        if new_filename is not None:
            self.filename = new_filename

    def write(self):
        with open(self.filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=";")

            writer.writerow(('Заголовок',
                             'Ссылка',
                             'Автор',
                             'Дата публикации',
                             'Количество лайков',
                             'Количество комментариев'))

            for data in self.data:
                writer.writerow(str(data).split(';'))
