from pathlib import Path
import os   
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUD_NAME"),
    'API_KEY': os.getenv("API_KEY"),
    'API_SECRET': os.getenv("API_SECRET"),
    'SECURE': True,
    'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'manifest')
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

SECRET_KEY = os.getenv("API_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [".onrender.com", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "index",
    "tailwind",
    "theme",
    'django_browser_reload',
    'boutique',
    'accounts',
    'adminsortable2',
    'analytics',
    'news',
    'cloudinary',
    'cloudinary_storage',
    "django.contrib.sitemaps",
    'annonces',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'analytics.middleware.AnalyticsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
                'index.context_processors.sponsors_context',
                'news.context_processors.latest_articles',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Tailwind config
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = "C:\Program Files\\nodejs\\npm.cmd"


# EMAIL CONFIG with SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# From address used by SendGrid
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration optionnelle pour WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
