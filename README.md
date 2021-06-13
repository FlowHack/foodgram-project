# Foodgram

Сайт: 
- _http://www.foodgram-prod.tk_
- _http://foodgram-prod.tk_
- _http://84.252.140.69/_

![example workflow](https://github.com/FlowHack/foodgram-project/actions/workflows/foodgram.yml/badge.svg)

### Описание
_Благодаря этому ресурсу каждый сможет найти для себя вкусненький рецепт или поделиться своим_

### Технологии
- Python 3.8
- Django==3.2.3
- Gunicorn==20.1.0
- Nginx==1.19.3

### Запуск проекта
- Установите [Docker](https://docs.docker.com/engine/install/) на свой сервер
- Из репозитория закиньте в одну папку файл docker-compose.yaml и папку nginx
- В файле default.conf из папки nginx измените строкy, где IP - ip вашего сервера, доменное имя.
```
server_name IP;
```
- Запустите docker из папки
```
docker-compose up
```
- Узнайте ID своего контейнера
```
docker ps
```
- Войдите в bash своего контейнера 
```
docker exec -it container_id bash
```
- Выполните команды
```
python3 manage.py makemigrations Users
python3 manage.py makemigrations Recipes
python3 manage.py makemigrations
python3 manage.py migrate
```
- Создайте супер пользователя (следуйте инструкциям)
```
python3 manage.py createsuperuser
```
- Заполните БД стартовыми данными (по желанию)
```
python3 manage.py loaddata fixtures/ingredients.json
python3 manage.py loaddata fixtures/tags.json
python3 manage.py loaddata fixtures/flatpages.json
python3 manage.py loaddata fixtures/recipes.json
```
- Выйдите из bash командой Ctrl + C

# Готово!