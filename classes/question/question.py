class Question:
    def __init__(self, text: str, key: str, values: tuple):
        self.text = text
        self.key = key
        self.values = values

    def give_response(self):
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



# pq = PromptQuestion('Изменить имя файла по умолчанию?\n1. Да;\n2. Нет;',
#                     'is_rename')
#
# print(pq.give_prompt())
