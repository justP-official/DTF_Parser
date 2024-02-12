from classes.question.question import Question


class BoolQuestion(Question):
    def __init__(self, text: str, key: str):
        values = (True, False)
        super().__init__(text, key, values)

    def __bool__(self):
        return self.give_response()[self.key]
