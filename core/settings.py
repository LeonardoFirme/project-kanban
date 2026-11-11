import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-kanban-secret-key-change-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'DB_KANBAN'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = False
USE_L10N = True
DATETIME_FORMAT = "d/m/Y H:i"
DATE_FORMAT = "d/m/Y"

LANGUAGES = (
    ('pt-br', _('Portuguese')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('de', _('German')),
    ('it', _('Italian')),
)

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UNFOLD = {
    "SITE_TITLE": "Kanban Admin",
    "SITE_HEADER": "Kanban",
    "SITE_URL": "/",
    "SITE_SYMBOL": "view_kanban",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_LANGUAGES": True,
    "THEME": "light",
    "BORDER_RADIUS": "8px",
    "DASHBOARD_CALLBACK": "projects.views.dashboard_callback",
    "SITE_DROPDOWN": [
        {
            "icon": "public",
            "title": _("Site público"),
            "link": reverse_lazy("projects:home"),
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "calendar_month",
            "title": _("Calendário"),
            "link": reverse_lazy("projects:calendar"),
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "task_alt",
            "title": _("Tarefas"),
            "link": reverse_lazy("projects:tasks"),
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "dashboard",
            "title": _("Painel"),
            "link": reverse_lazy("admin:index"),
        },
    ],
    "LANGUAGES": {
        "navigation": [
            {
                "bidi": False,
                "code": "pt-br",
                "name": "Portuguese",
                "name_local": "Português",
                "name_translated": "Português",
            },
            {
                "bidi": False,
                "code": "en",
                "name": "English",
                "name_local": "English",
                "name_translated": "English",
            },
            {
                "bidi": False,
                "code": "es",
                "name": "Spanish",
                "name_local": "Español",
                "name_translated": "Español",
            },
            {
                "bidi": False,
                "code": "de",
                "name": "German",
                "name_local": "Deutsch",
                "name_translated": "Deutsch",
            },
            {
                "bidi": False,
                "code": "it",
                "name": "Italian",
                "name_local": "Italiano",
                "name_translated": "Italiano",
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Painel"),
                "separator": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": _("Gerenciamento"),
                "separator": True,
                "items": [
                    {
                        "title": _("Projetos"),
                        "icon": "folder",
                        "link": "/admin/projects/project/",
                    },
                    {
                        "title": _("Tarefas"),
                        "icon": "task_alt",
                        "link": "/admin/projects/task/",
                    },
                    {
                        "title": _("Equipes"),
                        "icon": "group",
                        "link": "/admin/projects/team/",
                    },
                ],
            },
            {
                "title": _("Autenticação"),
                "separator": True,
                "items": [
                    {
                        "title": _("Usuários"),
                        "icon": "person",
                        "link": "/admin/auth/user/",
                    },
                    {
                        "title": _("Grupos"),
                        "icon": "admin_panel_settings",
                        "link": "/admin/auth/group/",
                    },
                ],
            },
        ],
    },
}