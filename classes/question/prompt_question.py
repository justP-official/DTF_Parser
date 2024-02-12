from classes.question.bool_question import BoolQuestion


class PromptQuestion(BoolQuestion):
    def __init__(self, text: str, key: str):
        super().__init__(text, key)

        self.prompt = None

    def give_prompt(self):
        if self:
            print("Введите имя файла: ____________.csv")
            self.prompt = f"{input('>> ')}.csv"

        return self.prompt
