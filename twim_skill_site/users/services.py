import logging

import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)


def get_steam_faceit_user_data(user: AbstractUser) -> dict:
    """Получить данные пользователя Steam и FaceIt"""

    steam_user_data = None
    faceit_user_data = None

    if user.is_authenticated and not user.is_superuser:
        # Получение данных Steam
        steam_user_data = SocialAccount.objects.filter(user=user)[0]
        user_steam_id = steam_user_data.extra_data.get('steamid')

        # Получение данных FaceIt
        request_for_faceit_data = 'https://api.faceit.com/search/v1/?limit=3&query=' + user_steam_id
        faceit_data = requests.get(request_for_faceit_data).json()
        faceit_user_data = faceit_data.get('payload', {}).get('players', {}).get('results')
        logger.info(f'user_steam_id={user_steam_id} | faceit_user_data = {faceit_user_data}')
        faceit_user_data = faceit_user_data[0] if faceit_user_data else None

    return {'steam_user_data': steam_user_data, 'faceit_user_data': faceit_user_data}
