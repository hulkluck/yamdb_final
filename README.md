# API_YaMDB

***

# WORKFLOW

![example workflow](https://github.com/hulkluck/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

***

### __Описание__

***

#### Технологии

1. [Django](https://www.djangoproject.com)
2. [Django Rest Framework](https://www.django-rest-framework.org)
3. SQlite
4. JWT авторизация
5. Docker

__API__ стремится к __RESTFUL__ и представляет собой проект, который собирает отзывы
на произведения, которые в свою очередь делятся по категориям.
***

#### Эндпоинты

* /redoc/ - Документация
* /api/v1/auth/signup/ - Создание пользователя(получение кода подтверждения)
* /api/v1/auth/token/ - Получение токена
* /api/v1/categories/ - Получение списка категорий
* /api/v1/genres/ - Получение списка жанров
* /api/v1/titles/ - Получение списка произведений
* /api/v1/titles/{id}/ - Подробная информация
* /api/v1/titles/{title_id}/reviews/ - Посмотреть || Добавить отзывы
* /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Посмотреть || Добавить комментарии к отзыву
* /api/v1/users/me/ - Информация о вашем аккаунте

***

### Для развёртывания

* docker-compose up -d --build
* docker-compose exec web python manage.py migrate
* docker-compose exec web python manage.py createsuperuser
* docker-compose exec web python manage.py collectstatic --no-input  

***

### Шаблон .env файла

* DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
* DB_NAME=postgres # имя базы данных
* POSTGRES_USER=postgres # логин для подключения к базе данных
* POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
* DB_HOST=db # название сервиса (контейнера)
* DB_PORT=5432 # порт для подключения к БД

***

###

* Об авторе:
* Привет всем =)
* Зовут меня Антон, учусь программировать на python.
* "Явное, лучше не явного" -_-

***

###

* License
* MIT @ Anton Bek
