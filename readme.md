
### Интернет-магазин на Django

#### Инструменты разработки


<span>`Django`</span>
<span>`DjangoRestFramework`</span>
<span>`Celery`</span>
<span>`NGINX`</span>
<span>`Gunircon`</span>

#### Установка:

<ol>
    <li>Создайте виртуальное окружение и активируйте его<pre><code>python -m venv env</code></pre><br></li>
    <li>Клонировать репозиторий<pre><code>git clone https://github.com/Untouchable17/Ecommerce-Shop.git</code></pre><br></li>
    <li>Установите все необходимые зависимости в проекте<pre><code>pip install -r requirements.txt</code></pre><br></li>
    <li>В файле .env заполните все необходимые поля<pre></pre><br></li>
    <li>Подготовьте модели к миграции<pre><code>python manage.py makemigrations</code></pre><br>
    <li>Запустите миграции<pre><code>python manage.py migrate</code></pre><br>
    <li>Создайте суперпользователя<pre><code>python manage.py createsuperuser</code></pre><br>
</ol>

#### Запуск на локальном сервере

> Запустите сайт<pre><code>python manage.py runserver</code></pre><br></li>


#### Запуск на продакшн сервере

> Запустите файл install.sh и заполните все поля

