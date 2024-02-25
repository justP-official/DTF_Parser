import csv

from classes.question.prompt_question import PromptQuestion


class Writer:
    """
    Класс для записи данных в csv-файл.

    Атрибуты
    --------
    data : list
        Список с данными, которые нужно записать в файл.
    filename : str
        Имя файла, в который будут записываться данные.

    Методы
    ------
    change_filename
        Меняет имя файла.
    write
        Записывает данные в файл.
    """
    def __init__(self, data: list):
        """
        Инициализация экземпляра класса Writer.

        Параметры
        ---------
        data : list
            Список с данными для записи

        Атрибуты
        --------
        filename : str
            Имя файла, в который будут записаны данные. По умолчанию: 'output.csv'.
        """
        self.data = data

        self.filename = 'output.csv'

    def change_filename(self) -> None:
        """
        Метод для изменения имени файла.

        Для функционала использует класс PromptQuestion, метод give_prompt.

        Если метод give_prompt вернул не None, то запрашивается доп. вопрос с требованием ввести имя файла.

        Возвращаемое значение
        ---------------------
        None
        """
        new_filename = PromptQuestion(
            f'Изменить имя файла по умолчанию? (По умолчанию: {self.filename})\n1. Да;\n2. Нет;',
            'is_rename',
            'Введите имя файла: ____________.csv'
        ).give_prompt()

        if new_filename is not None:
            self.filename = new_filename + ".csv"

    def write(self) -> None:
        """
        Метод для записи данных в файл.

        Для функционала использует модуль 'csv' стандартной библиотеки Python.

        При помощи контекстного менеджера открывает файл на запись, устанавливает кодировку 'utf-8-sig'.

        При помощи функции writer создаётся объект writer для записи данных.
        Устанавливаются параметры для разделителя и добавления кавычек.

        Возвращаемое значение
        ---------------------
        None
        """
        with open(self.filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=";")

            writer.writerow(('Заголовок',
                             'Ссылка',
                             'Автор',
                             'Дата публикации',
                             'Количество лайков',
                             'Количество комментариев'))

            for data in self.data:
                writer.writerow(data)
            else:
                print(f"Данные успешно записаны в {self.filename}")
