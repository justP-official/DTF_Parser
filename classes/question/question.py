class Question:
    """
    Класс для взаимодействия пользователя с программой.

    Атрибуты
    --------
    text : str
        Текст вопроса.
    key : str
        Ключевая фраза.
    values : tuple
        Варианты ответа.

    Методы
    ------
    give_response
        Получает ответ на заданный вопрос.
    """
    def __init__(self, text: str, key: str, values: tuple):
        """
        Инициализация экземпляра класса Question.

        Параметры
        ---------
        text : str
            Текст вопроса.
        key : str
            Ключевая фраза. Используется для дальнейшей манипуляции с ответом.
        values : tuple
            Варианты ответа.
        """
        self.text = text
        self.key = key
        self.values = values

    def give_response(self) -> dict:
        """
        Метод для выбора ответа из предложенных вариантов.

        Для того чтобы пользователь гарантированно выбрал вариант ответа, запускается бесконечный цикл.
        Пока пользователь не выберет подходящий вариант, цикл не прекратится.

        Возвращаемое значение
        ---------------------
        dict
            Словарь, ключом которого является ключевая фраза, а значением один из вариантов ответа.
        """
        while True:
            print(self)
            try:
                response = int(input(">> ")) - 1
            except ValueError:
                print("Неверный ответ. Попробуйте снова.")
                continue

            if 0 <= response < len(self.values):
                return {self.key: self.values[response]}
            else:
                print("Неверный ответ. Попробуйте снова.")

    def __str__(self):
        return self.text
