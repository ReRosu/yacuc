# Пример приложения для графиков для Udav Conf #1

### Автор
- https://t.me/rcr_tg

### Сообщество Python Уфа
- https://t.me/ufa_python

### Ссылка на доклад
- https://docs.google.com/presentation/d/1ekWWN_OHUfayF0REJm9FCIrTbV7UK-lY8ZtviaS9YL4/edit?usp=sharing

### Установка зависимостей через Poetry
~~~
poetry install
~~~


### Настройка .env
~~~
nano .env
~~~
Вставьте в .env следующее
~~~
clickhouse_user=...
clickhouse_password=...
clickhouse_database=...
clickhouse_host="localhost"
clickhouse_port=8123
postgres_db=...
postgres_port=5432
postgres_host="localhost"
postgres_user=...
postgres_password=...
reload=false
~~~


### Поднятие баз данных 
~~~
docker compose up --build -d
~~~


### Настройка баз данных
~~~
Для постгреса сначала выполняем то что лежит в lttb.sql, затем pg_setup.sql
Для кликхауса выполняем ch_setup.sql
~~~


### Для запуска приложения
~~~
poetry run python main.py
~~~
- Потом заходим на http://localhost:8080/plots
