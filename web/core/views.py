from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View

from .backend import TgAuthUserBackend
from .models import User
from .forms import ChangePasswordForm
#from web.core.context_processors.widget_generator import tg_login_widget


bot_name = settings.TELEGRAM_BOT_NAME
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL
LARGE = 'large'
DISABLE_USER_PHOTO = False


class IndexView(View):

    @staticmethod
    def get(request):
        context = {'hello': 'Привет=Р'}
        template = 'index.html'
        return render(request, template, context)


def login(request):
    """ Страница для размещения всх вариантов входа в систему"""
    return render(request, 'registration/login.html', context={})


class UserDetail(LoginRequiredMixin, DetailView):
    """Страница профиля пользователя"""
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = User

    def a_change_password(request):
        u = User.objects.get(username=request.user)
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = request.POST.get("old_password")
                new_pass = request.POST.get("new_password")
                new_pass_rep = request.POST.get("new_password_repeat")
                if check_password(old_password, u.password):
                    return HttpResponse('ok')
                else:
                    return HttpResponse('bad')
        else:
            form = ChangePasswordForm()

        return render(request, 'login/change_password.html',
                      {'form': form, 'user': u})



def auth(request):
    """
    Функция проверки запроса, отправки данных на авторизацию и перенаправления в профиль
    пользователя
    """
    if not request.GET.get('hash'):
        print('проблема с данными')  # нужно исправить на что-то удобоваримое для юзверей
        return redirect('/')
    else:
        # user_id_tg = request.GET.get('id')
        user = TgAuthUserBackend.autentificate(request, request)
        return redirect(f'/profile/{user.username}')
