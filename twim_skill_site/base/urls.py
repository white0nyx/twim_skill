from allauth.account import views
from django.urls import path

from base.views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path("logout/", views.logout, name="account_logout")
]