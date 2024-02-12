from classes.parser.parser import Parser

from classes.question.bool_question import BoolQuestion

from classes.writer.writer import Writer

if __name__ == '__main__':
    p = Parser(input('Введите поисковый запрос: '))
    p.search()

    is_write = BoolQuestion("Записать данные в файл?\n1. Да;\n2. Нет;", 'is_write')

    if is_write:
        writer = Writer(p.useful_data)
        writer.change_filename()
        writer.write()

    for i, post in enumerate(p.useful_data):
        print(i + 1, post, '\n')
