
### Интернет-магазин на Django

#### Инструменты разработки


<span>`Django`</span>
<span>`DjangoRestFramework`</span>
<span>`Celery`</span>
<span>`NGINX`</span>
<span>`Gunircon`</span>

#### Установка:


1. Создайте виртуальное окружение и активируйте его `python -m venv venv` и `source venv/bin/activate`
2. Скачайте репозиторий `https://github.com/Untouchable17/Ecommerce-Shop.git`
3. Установите все зависимости `pip install -r requirements.txt`
4. В файле `.env` заполните все необходимые поля
5. Создайте миграции в базе данных `python manage.py makemigrations`
6. Примените созданные миграции `python manage.py migrate`
7. Создайте суперпользователя `python manage.py createsuperuser`

#### Запуск на локальном сервере

1. Запустите сайт `python manage.py runserver`


#### Запуск на продакшн сервере

1. Запустите bash файл `install.sh` и заполните все поля
2. В NGINX файле укажите путь к статическим файлам

