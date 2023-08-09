from allauth.socialaccount.models import SocialAccount
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
import requests


def get_all_user_data(request: WSGIRequest):
    """Формирование всех данных пользователя"""

    user_data = None
    faceit_user_data = None

    if request.user.is_authenticated:
        user_data = SocialAccount.objects.filter(user=request.user)

        # Проверка на то, является ли пользователь админом
        if user_data:
            user_data = user_data[0]

            user_steam_id = user_data.extra_data.get('steamid')

            # Получение данных FaceIT по Steam ID
            request_for_faceit_data = 'https://api.faceit.com/search/v1/?limit=3&query=' + user_steam_id
            faceit_user_data = requests.get(request_for_faceit_data).json().get('payload').get('players').get('results')

            if faceit_user_data:
                faceit_user_data = faceit_user_data[0]

    return {'user_data': user_data, 'faceit_user_data': faceit_user_data}


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""
        context = {}
        context.update(get_all_user_data(request))
        return render(request, 'main/main.html', context)


class ProfilePage(DetailView):
    """Класс представления страницы профиля пользователя"""
    model = SocialAccount
    template_name = 'main/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """Обработка get-запроса"""

        # Редирект для администраторов
        if request.user.is_superuser:
            return render(request, 'main/admin_profile.html')

        # Редирект на главную, если пользователь не авторизован
        if not request.user.is_authenticated:
            return redirect('main')

        context = {}
        context.update(get_all_user_data(request))
        return render(request, 'main/profile.html', context)
