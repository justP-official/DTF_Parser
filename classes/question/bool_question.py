from classes.question.question import Question


class BoolQuestion(Question):
    """
    Наследуется от класса Question, расширяет его.

    Класс для получения однозначного ответа на вопрос: Да или Нет.

    Переопределяет магический метод __bool__.

    Смотри также
    ------------
    Question
    """

    def __init__(self, text: str, key: str):
        """
        Инициализация экземпляра класса BoolQuestion.

        Параметры
        ---------
        text : str
            Текст вопроса.
        key : str
            Ключевая фраза.

        Атрибуты
        --------
        values : tuple
            Кортеж, в котором хранятся варианты ответов. Так как это логический класс, содержит булевы значения.
        """
        values = (True, False)
        super().__init__(text, key, values)

    def __bool__(self) -> bool:
        """
        Метод для дачи однозначного ответа на вопрос.

        Вызывает метод give_response родительского класса.

        Возвращаемое значение
        ---------------------
        bool
            Ответ на вопрос.
        """
        return self.give_response()[self.key]
