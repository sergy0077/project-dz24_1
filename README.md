


## Инструкции по запуску Docker compose
- описать Dockerfile для запуска контейнера с проектом.
- обернуть в Docker Compose Django-проект с БД PostgreSQL.
- дописать в docker-compose.yaml работу с Redis.
- дописать в docker-compose.yaml работу с Celery.
- установить все зависимости в requirements.txt.
- собрать ваш Docker образ командой в терминале: docker-compose build
- выполнить миграции командой: docker-compose run app python manage.py migrate
- поднять (запустить) ваши Docker контейнеры командой:  docker-compose up



