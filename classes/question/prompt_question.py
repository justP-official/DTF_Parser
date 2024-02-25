from classes.question.bool_question import BoolQuestion


class PromptQuestion(BoolQuestion):
    """
    Наследуется от класса BoolQuestion, расширяет его.

    Класс для получения конкретного ответа на вопрос.

    Атрибуты
    --------
    sub_question: str
        Текст дополнительного вопроса.
    prompt : str or None
        Конкретный ответ на вопрос.

    Методы
    ------
    give_prompt : str or None
        Метод для получения конкретного ответа.

    Смотри также
    ------------
    BoolQuestion
    """

    def __init__(self, text: str, key: str, sub_question: str):
        """
        Инициализация экземпляра класса PromptQuestion.

        Параметры
        ---------
        text : str
            Текст вопроса.
        key : str
            Ключевая фраза.
        sub_question : str
            Дополнительный вопрос.

        Атрибуты
        --------
        sub_question : str
            Текст дополнительного вопроса.
        prompt : str or None
            Конкретный ответ на вопрос. По умолчанию None.
        """
        super().__init__(text, key)

        self.sub_question = sub_question
        self.prompt = None

    def give_prompt(self) -> str or None:
        """
        Метод для получения конкретного ответа на вопрос.

        Вначале задаётся вопрос: нужен ли конкретный ответ?

        Если да, то пользователю нужно ввести ответ.

        Возвращаемое значение
        ---------------------
        str если пользователь ввёл ответ, иначе None.
        """
        if self:
            print(self.sub_question)
            self.prompt = input('>> ')

        return self.prompt
