from django.urls import path

from lobby.views import *

urlpatterns = [

    # Страницы сайта
    path('create_lobby/', CreateLobbyPage.as_view(), name='create_lobby'),
    path('leave_f_lobby/', leave_from_lobby, name='leave_f_lobby'),
    path('detail_lobby/<slug:slug>/', DetailLobbyPage.as_view(), name='detail_lobby'),
    path('join_lobby/<slug:slug>/', JoinLobby.as_view(), name='join_lobby'),
    path('game_action/', game_action, name='game_action'),
    path('join_team/', join_team, name='join_team'),

    # API-запросы
    path('api/v1/lobbies_list', LobbyAPIView.as_view())
]