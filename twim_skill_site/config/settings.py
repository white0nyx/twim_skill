"""
Django settings for twim_skill_site project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from environs import Env

# Подгрузка конфиденциальных переменных
env = Env()
env.read_env('.env')
STEAM_TOKEN = env.str('STEAM_TOKEN')

POSTGRESQL_DB_NAME = env.str('POSTGRESQL_DB_NAME')
POSTGRESQL_DB_USER = env.str('POSTGRESQL_DB_USER')
POSTGRESQL_DB_PASSWORD = env.str('POSTGRESQL_DB_PASSWORD')
POSTGRESQL_DB_HOST = env.str('POSTGRESQL_DB_HOST')
POSTGRESQL_DB_PORT = env.str('POSTGRESQL_DB_PORT')

# Пути сборки внутри проекта выглядят следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: храните секретный ключ, используемый в производстве, в тайне!
SECRET_KEY = 'django-insecure-xkpyfo8&mu9n77ztw^o$co(j_b-!4m%6c($w#4n_n#q5=1m62h'

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: не работайте с включенной отладкой в production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Наши приложения
    'main.apps.MainConfig',
    'users.apps.UsersConfig',

    # Авторизация
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.steam',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRESQL_DB_NAME,
        'USER': POSTGRESQL_DB_USER,
        'PASSWORD': POSTGRESQL_DB_PASSWORD,
        'HOST': POSTGRESQL_DB_HOST,
        'PORT': POSTGRESQL_DB_PORT,
    }
}

# Авторизация
AUTHENTICATION_BACKENDS = [
    # Необходим для входа по имени пользователя в админку Django, независимо от `allauth`.
    'django.contrib.auth.backends.ModelBackend',
    # Специфические методы аутентификации, такие как вход по электронной почте
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Редирект после авторизации
LOGIN_REDIRECT_URL = '/'

# Валидаторы паролей
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Для авторизации
SITE_ID = 1

# С таким параметром происходит вход, но есть ошибки
SOCIALACCOUNT_PROVIDERS = {
    'steam': {
        'APP': {
            'client_id': STEAM_TOKEN,
            'secret': STEAM_TOKEN,
            'key': STEAM_TOKEN
        }
    }
}

# Уровни логирования
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'myformatter': {
            'format': '{asctime} | {levelname} | {filename} | {funcName} | {thread:d} | {message}',
            'style': '{'
        }
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'sites_logs.log',
            'formatter': 'myformatter'

        }
    },

    'loggers': {
        'main': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

# Используемая модель пользователя
AUTH_USER_MODEL = 'users.User'

