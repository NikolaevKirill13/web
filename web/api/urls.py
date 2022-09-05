from django.urls import path, re_path
from .views import apiOverview, FaqList, FaqDetail, BlockWriteDetail, UserWriteList, UserWriteDetail,\
    BlockWriteList, PollWriteList, PollDetailList, authenticate_bot




urlpatterns = [
    path('', apiOverview),
    path('login/', authenticate_bot),
    path('faq', FaqList.as_view()),
    path('faq/<str:title>', FaqDetail.as_view()),
    path('block', BlockWriteList.as_view()),
    re_path(r'^block/(?P<user>\d+)$', BlockWriteDetail.as_view()),
    path('user', UserWriteList.as_view()),
    re_path(r'^user/(?P<user_id_tg>\d+)$', UserWriteDetail.as_view()),
    path('poll', PollWriteList.as_view()),
    re_path(r'^poll/(?P<keyboard_id>\d+)$', PollDetailList.as_view()),


]
