import requests
from rest_framework.response import Response



def post_user():
    """
    Запрос POST на добавление юзверя в БД.
    """
    url = 'http://127.0.0.1:8000/api/user'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJzdCIsImV4cCI6MTY1ODgzMjU2OSwiZW1haWwiOiIifQ.LAYd3Y683-bJbA6OxHZp_O05JaTq1O-V8lm4ODU2dBI"
    headers = {"Authorization": f"Bearer {token}"}
    data = {'username': 'zxczxc', 'first_name': '', 'last_name': '', 'user_id_tg': '9999', 'warn': '0'}
    send = requests.post(url=url, data=data, headers=headers)
    return send


def post_poll():
    """
    Запрос POST на добавление голосования. Отправляем ид клавиатуры и ид кто проголосовал.
    В ответ придет ид голосования, кто проголосовал и общее количество голосовавших. Повторы не будут учитываться
    Запрос GET вернет все созданные голосования, запрос GET api/poll/id голосования вернет само голосование
    """
    url = 'http://127.0.0.1:8000/api/poll'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJzdCIsImV4cCI6MTY1ODgzMjU2OSwiZW1haWwiOiIifQ.LAYd3Y683-bJbA6OxHZp_O05JaTq1O-V8lm4ODU2dBI"
    headers = {"Authorization": f"Bearer {token}"}
    data = {'keyboard_id': '123', 'user_id': '112233'}
    send = requests.post(url=url, data=data, headers=headers)
    return send


def post_block():
    """
    Запрос на добавление юзверя в мут. Нужно только для записи в БД, общей статистики. Добавляет только существующего
    юзверя. Если в ответ на добавление приходит "detail": "Страница не найдена" - то такого юзверя в базе нет
    """
    url = 'http://127.0.0.1:8000/api/block'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJzdCIsImV4cCI6MTY1ODgzMjU2OSwiZW1haWwiOiIifQ.LAYd3Y683-bJbA6OxHZp_O05JaTq1O-V8lm4ODU2dBI"
    headers = {"Authorization": f"Bearer {token}"}
    data = {'user': '300', 'permanent': False}
    send = requests.post(url=url, data=data, headers=headers)
    return send

def login_token():
    """
    Изначально надо зайти в админку и создать там юзера для Бота.
     Проще всего создавать юзера с username - имя бота, password - так же имя бота и использовать
    в переменных их bot_name и bot_password. В ответ на логин придет словарь, содержащий имя бота и токен, который
    нужно использовать при запросах на другие методы api. Слеш в конце адреса обязателен!!!
    """
    bot_name = 'st'
    bot_password = '130982'
    data = {'username': f'{bot_name}', 'password': f'{bot_password}'}
    url = 'http://127.0.0.1:8000/api/login/'  # косая черта в запросе на логин в конце обязательна!
    send = requests.post(url=url, data=data)
    print(Response.getvalue(self=send))
    return send

def faq_list():
    """
    Тестируем получение справки с авторизацией"""
    url = "http://127.0.0.1:8000/api/faq"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJzdCIsImV4cCI6MTY1ODgzMjU2OSwiZW1haWwiOiIifQ.LAYd3Y683-bJbA6OxHZp_O05JaTq1O-V8lm4ODU2dBI"
    headers = {"Authorization": f"Bearer {token}"}
    send = requests.get(url=url, headers=headers)
    print(Response.getvalue(self=send))
    return send

def faq_add():
    """
    Добавление справки в БД. Остальные методы по аналогии без data
    """
    url = "http://127.0.0.1:8000/api/faq"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJzdCIsImV4cCI6MTY1ODgzMjU2OSwiZW1haWwiOiIifQ.LAYd3Y683-bJbA6OxHZp_O05JaTq1O-V8lm4ODU2dBI"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": "test2", "description": "test2"}
    send = requests.post(url=url, data=data, headers=headers)
    print(Response.getvalue(self=send))
    return send


#post_user()
#post_faq()
#post_poll()
#post_block()
#faq_list()
#login_token()
#faq_add()