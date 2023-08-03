from django.shortcuts import render
from django.views.generic import ListView


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'main/main.html', context)
