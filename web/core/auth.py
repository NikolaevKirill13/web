"""
Telegram login authentication functionality.
"""
import hashlib
import hmac
from django.contrib.auth import settings


def NotTelegramDataError():
    pass


def chek_authentication(request_data):
    """
    Check if received data from Telegram is real.

    Based on SHA and HMAC algothims.
    Instructions - https://core.telegram.org/widgets/login#checking-authorization
    """
    request_data = request_data.copy()
    bot_token = settings.TELEGRAM_BOT_TOKEN
    received_hash = request_data['hash']

    request_data.pop('hash', None)
    request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

    data_check_string = []

    for data_pair in request_data_alphabetical_order:
        key, value = data_pair[0], data_pair[1]
        data_check_string.append(key + '=' + value)

    data_check_string = '\n'.join(data_check_string)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    if _hash == received_hash:
        return True
    else:
        return False


