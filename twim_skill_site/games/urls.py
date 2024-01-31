from django.urls import path

from games.views import *

urlpatterns = [

    # Страницы сайта
    # ...

    # API-запросы
    path('api/v1/games_list', GameAPIList.as_view()),
    path('api/v1/game_update/<int:pk>/', GameAPIUpdate.as_view()),

    path('api/v1/matches_list', MatchAPIList.as_view())
]