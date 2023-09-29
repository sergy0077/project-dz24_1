Данное домашнее задание касается разработки LMS-системы, в которой каждый желающий может размещать свои полезные материалы или курсы.
Теперь работа будет над SPA-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры.

Задание 1
Создайте новый Django-проект, подключите DRF и внесите все необходимые настройки.
Задание 2
Создайте следующие модели:
Пользователь:
все поля от обычного пользователя, но авторизацию заменить на email;
телефон;
город;
аватарка.
Курс:
название,
превью (картинка),
описание.
Урок:
название,
описание,
превью (картинка),
ссылка на видео.
Задание 3
Опишите CRUD для моделей курса и урока, но при этом для курса сделайте через ViewSets, а для урока — через Generic-классы.
Для работы контроллеров опишите простейшие сериализаторы.
Работу каждого эндпоинта необходимо проверять с помощью Postman.
Также на данном этапе работы мы не заботимся о безопасности и не закрываем от редактирования объекты и модели даже самой простой авторизацией.

## Программные требования
Установите пакеты из файла requirements.txt
- `Django`
- `psycopg2`
- `pillow`
- `djangorestframework`


## Пресеты
Создайте миграции базы данных командой: python manage.py migrate.
Перед запуском проекта создайте суперпользователя

## Запуск
Запустите проект командой: python manage.py runserver в терминале.
Переходите по ссылке: http://127.0.0.1:8000/ и начинайте использование проекта 


