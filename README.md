# Парсер DTF
_Парсер результатов поискового запроса сайта "dtf.ru"._
## Стэк: 
+ Python
+ ~~Selenium~~
+ bs4
+ requests

----

## История версий:
1. ### v0.1: Рабочий прототип
   + v0.1.2: Изменена файловая структура
   + v0.1.3: Класс "Post" переделан в дата-класс
2. ### v0.2: Полный отказ от Selenium, переход на requests
   + v0.2.2: Теперь собираются лайки и комментарии (опять)
   + v0.2.3: Удалены веб-драйвера для Selenium
3. ### v0.3: Добавлена поддержка расширенного поиска
   + v0.3.2: Мелкие правки
   + v0.3.3: Удалены излишние атрибуты и методы
4. ### v0.4: Добавлена возможность записи данных в csv-файл