from pathlib import Path
import environ
from django.contrib.messages import constants as messages

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))


APPS_DIR = BASE_DIR / "apps"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

# ALLOWED_HOSTS = []

# if not DEBUG:
ALLOWED_HOSTS = ["www.quranutla.com", "quranutla.com"]


# Application definition

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jazzmin",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "django_cleanup.apps.CleanupConfig",
    "django_summernote",
    "phonenumber_field",
    # "crispy_forms",
]

LOCAL_APPS = [
    "apps.dashboard",
    "apps.about",
    "apps.main",
    "apps.course",
    "apps.blog",
    "apps.learning",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.context.context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# if not DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": env("POSTGRES_DB"),
#             "USER": env("POSTGRES_USER"),
#             "PASSWORD": env("POSTGRES_PASSWORD"),
#             "HOST": env("POSTGRES_HOST"),
#             "PORT": env("POSTGRES_PORT"),
#         }
#     }

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = str(BASE_DIR / "static")
STATIC_URL = "/staticfiles/"
STATICFILES_DIRS = [str(APPS_DIR / "staticfiles")]


MEDIA_ROOT = "/home/eslam/media/"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


JAZZMIN_SETTINGS = {
    "site_title": "Quran utl",
    "site_header": "Quran utl",
    "site_brand": "Quran utl",
    "welcome_sign": "Welcome Quran utl",
    "copyright": "by :Eslam Es",
    "topmenu_links": [
        {"name": "Home", "url": "/"},
    ],
}


MESSAGE_TAGS = {
    messages.DEBUG: "alert",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}


AUTH_USER_MODEL = "dashboard.CustomUser"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Keep the default backend if needed
    "apps.dashboard.backends.PhoneBackend",  # Add your custom backend
)

# SESSION_COOKIE_AGE = 300

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True


LOGIN_URL = "/dashboard/login/"

LOGOUT_REDIRECT_URL = "/dashboard/login/"

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": "debug.log",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console", "file"],
#             "level": "DEBUG",
#         },
#     },
# }


PHONENUMBER_DEFAULT_REGION = "US"
