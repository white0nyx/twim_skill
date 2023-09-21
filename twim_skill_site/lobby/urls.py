from django.urls import path

from lobby.views import *

urlpatterns = [
    path('create_lobby/', CreateLobbyPage.as_view(), name='create_lobby'),
    path('leave_f_lobby/', leave_f_lobby, name='leave_f_lobby'),
    path('detail_lobby/<slug:slug>/', DetailLobbyPage.as_view(), name='detail_lobby'),
    path('join_lobby/<slug:slug>/', JoinLobby.as_view(), name='join_lobby'),
]