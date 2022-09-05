from time import time
import requests
from config import config
#WEB_URL = "http://127.0.0.1:8000/" text url


def get_warn(user_id) -> dict:
    url = config.WEB_URL + f"api/block/{user_id}?format=json"
    warn = requests.get(url=url)
    return warn.json()


def mute_time(user_id):
    warn = get_warn(user_id=user_id)["warn"]
    _time = time() + warn * 600 + (warn - 1) * 600
    return abs(_time)


def get_faq() -> list:
    url = config.WEB_URL + "api/faq?format=json"
    response = requests.get(url=url)
    content = response.json()
    return content


def push_user(user) -> bool:
    url = config.WEB_URL + "api/user"
    params = {"user_id":f"{user.id}", "first_name":f"{user.first_name}", "full_name":f"{user.full_name}", "username":f"{user.mention}",}
    response = requests.post(url=url, params=params)
    return True if response.code == 200 else False