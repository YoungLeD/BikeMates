Welcome to BikeMates!
===================


Этот мини-урок является инструкцией для настройки рабочего места 

----------


Подготовка
-------------
####  Загрузка проекта
Первым делом необходимо скачать репозиторий, в примере будем все делать в домашнем каталоге. Для этого пишем в консоли:

```bash
$ git clone git@gitlab.informatics.ru:smirnov/prom2016_32.git
```
#### Pip
Для будущей установки virtualenv и необходимых пакетов установим pip
```bash
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip 
```
#### Создание окружения

Теперь установим virtualenv
```bash
sudo pip install --upgrade virtualenv 
```
Создадим папку venvs, куда установим виртуальное окружение, затем активируем его
```bash
$ mkdir venvs
$ cd venvs
$ virtualenv -p /usr/bin/python3 mps
$ source mps/bin/activate
```
Установим необходимые пакеты из requirements.txt
```bash
$ pip install -r ~/prom2016_32/requirements.txt
```
#### Загрузка и установка PyCharm
Скачаем PyCharm по этой ссылке:
http://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC

Разархивируем загруженный архив:
```bash
$ tag.zr tar -zxvf Downloads/pycharm-community-2016-3.2.gz
```
#### Создание и настройка базы данных
В данном шаге первая часть может зависеть от ОС. Здесь приведены инструкции для 
Linux и macOS


##### Инструкция для пользователей Linux
Установим PostgreSQL:
```bash
$ sudo apt-get install postgresql
```
Зайдем в консоль postgreSQL:
```bash
$ sudo -u postgres psql
```

-------------------------

##### Инструкция для пользователей macOS
Установим утилиту Homebrew, с помощью которой потом скачаем postgreSQL:
```bash
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Скачаем postgreSQL:
```bash
$ brew install postgresql
```
Заходим в консоль postgreSQL:
```bash
$ psql -U postgres
```
-------------------------

После выполнения входа в консоль выполняем команды, с помощью которых добавляем 
БД bikemates, пользователя bikemates с паролем bikemates
```sql
CREATE DATABASE bikemates;
CREATE USER bikemates WITH password 'bikemates';
GRANT ALL privileges ON DATABASE bikemates TO bikemates;
```


https://stackedit.io/editor