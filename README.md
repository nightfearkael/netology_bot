# netology_bot

## Перед началом работы нужно:

### 1. Установить все зависимости из requirements.txt

### 2. Создать файл окружения .env со строками:

bot_token = '{Токен бота}'

db_host = '{Адрес СУБД (обычно localhost)}'

db_port = '{Порт СУБД}'

db_database = '{Имя базы данных}'

db_user = '{Пользователь базы данных}'

db_password = '{Пароль от пользователя}'

### 3. Создать и заполнить базу данных:

В папке ./manage_db выполнить по очереди скрипты create_DB.py и fill_DB.py

### 4. Запустить бота bot.py
