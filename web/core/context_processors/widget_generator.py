from django.conf import settings
"""
Widgets generator
"""


def tg_login_widget(request):
    WIDGET_SCRIPT_START = '<script async src="https://telegram.org/js/telegram-widget.js?19" '
    WIDGET_SCRIPT_END = '></script>'
    HOST = settings.HOST
    TELEGRAM_LOGIN_REDIRECT_URL = settings.TELEGRAM_LOGIN_REDIRECT_URL
    SIZE = 'large'
    data_auth_url = 'data-auth-url="{}" '.format(HOST + TELEGRAM_LOGIN_REDIRECT_URL)
    data_telegram_login = 'data-telegram-login="{}" '.format(settings.TELEGRAM_BOT_NAME)
    data_size = 'data-size="{}" '.format(SIZE)
    data_request_access = 'data-request-access="write"'
    widget = WIDGET_SCRIPT_START \
        + data_telegram_login \
        + data_size \
        + data_auth_url \
        + data_request_access \
        + WIDGET_SCRIPT_END
    return {'widget': widget}
