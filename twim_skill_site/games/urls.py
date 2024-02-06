from django.urls import path

from games.views import *

urlpatterns = [

    # Страницы сайта
    # ...

    # API-запросы
    path('api/v1/games_list', GameAPIView.as_view()),
    path('api/v1/matches_list', MatchAPIView.as_view())
]