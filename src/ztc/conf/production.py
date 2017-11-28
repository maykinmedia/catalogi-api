from .base import *
import raven

#
# Standard Django settings.
#

DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ztc',
        'USER': 'ztc',
        'PASSWORD': 'ztc',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i3yihsrle$16%4_&0_ic5psrzih+ostvzkzn7zwj$qddcl18+j'

ALLOWED_HOSTS = []

# Redis cache backend
# NOTE: If you do not use a cache backend, do not use a session backend or
# cached template loaders that rely on a backend.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2", # NOTE: watch out for multiple projects using the same cache!
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# Caching sessions.
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = "default"

# Caching templates.
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', RAW_TEMPLATE_LOADERS),
]

# The file storage engine to use when collecting static files with the
# collectstatic management command.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Production logging facility.
LOGGING['loggers'].update({
    '': {
        'handlers': ['sentry'],
        'level': 'ERROR',
        'propagate': False,
    },
    'django': {
        'handlers': ['django'],
        'level': 'INFO',
        'propagate': True,
    },
    'django.security.DisallowedHost': {
        'handlers': ['django'],
        'level': 'CRITICAL',
        'propagate': False,
    },
})

#
# Custom settings
#

# Show active environment in admin.
ENVIRONMENT = 'production'
SHOW_ALERT = False

# We will assume we're running under https
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
# Only set this when we're behind Nginx as configured in our example-deployment
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#
# Library settings
#

# Raven
INSTALLED_APPS = INSTALLED_APPS + [
    'raven.contrib.django.raven_compat',
]
RAVEN_CONFIG = {
    'dsn': 'https://',
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
LOGGING['handlers'].update({
    'sentry': {
        'level': 'WARNING',
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': RAVEN_CONFIG['dsn']
    },
})
