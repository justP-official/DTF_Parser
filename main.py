from classes.parser.parser import Parser

if __name__ == '__main__':
    p = Parser(input('Введите поисковый запрос: '))
    p.search()

    for i, post in enumerate(p.useful_data):
        print(i + 1, post, '\n')
