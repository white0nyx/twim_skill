from django.urls import path

from users.views import *

urlpatterns = [

    # Страницы сайта
    # ...

    # API-запросы
    path('api/v1/users_list', UserAPIView.as_view()),
]
