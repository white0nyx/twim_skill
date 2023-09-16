"""twim_skill_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib import import_module

from allauth import app_settings
from allauth.account import views
from allauth.socialaccount import providers
from django.contrib import admin
from django.urls import path, include, re_path

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', MainPage.as_view(), name='main'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('create_lobby/', CreateLobby.as_view(), name='create_lobby'),
    path('leave_f_lobby/', leave_f_lobby, name='leave_f_lobby'),
    path('detail_lobby/<slug:slug>/', DetailLobby.as_view(), name='detail_lobby'),
    path('join_lobby/<slug:slug>/', JoinLobby.as_view(), name='join_lobby'),
    path("logout/", views.logout, name="account_logout")
]



# URL для социальных сетей. В частности Steam.
if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns

urlpatterns += provider_urlpatterns
