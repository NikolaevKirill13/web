from django.urls import path
from .views import login, auth, IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('login/', login),
    path('login/auth/', auth),
]
