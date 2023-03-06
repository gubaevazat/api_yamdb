## API-YAMDB
Проект **api_yamdb** это REST API сервис, позволяющий просматривать, оставлять, редактировать отзывы,комментарии и ставить оценки к различным произведениям (фильмы, книги, музыка и т.д.). Для незарегистрированных пользователей доступен только просмотр.

## Использованные технологии

 - Python
 - Django
 - Django REST framework

## Установка и запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

    git clone https://github.com/gubaevazat/api_yamdb.git
    cd api_final_yatube
 Cоздать и активировать виртуальное окружение:

    python -m venv venv
    source venv/bin/activate
 Обновить пакетный менеджер проекта:

    python -m pip install --upgrade pip

 Установить зависимости из файла requirements.txt:

    pip install -r requirements.txt

Перейти в директорию с файлом `manage.py`:

    cd yatube_api

Выполнить миграции:

    python manage.py migrate

Запустить проект:

    python manage.py runserver

## Возможности и примеры запросов:
Неавторизованным пользователям возможен только просмотр контента. Для добавления, изменения и удаления нужно зарегистрироваться. Все возможные примеры запросов и ответов, а также права доступа, описаны в документации в формате ReDoc.
Для просмотра документации на локальном компьютере после запуска сервиса:

    python manage.py runserver
нужно перейти по адресу:

    http://127.0.0.1:8000/redoc/

Для тестирования проекта в директории `/api_yamdb/static/data`, подготовлены несколько файлов в формате `csv` с контентом для ресурсов **Users**, **Titles**, **Categories**, **Genres**, **Reviews** и **Comments**.
Для загрузки необходимо выполнить команду:

    python manage.py csv_import
Если возникают ошибки при загрузке нужно выполнить следующую последовательность команд:

  Удалить все папки с миграциями, удалить файл базы данных `db.sqllite3`. В терминале выполнить команды в следующем порядке:

    python manage.py makemigrations user
    python manage.py migrate user
    python manage.py makemigrations reviews
    python manage.py migrate reviews