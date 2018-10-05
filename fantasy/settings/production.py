from .base import *
import dj_database_url
# DEBUG = False

ALLOWED_HOSTS = ['fantasyplayers.herokuapp.com', ] #DONE change with the site
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'   #TODO change with the required values
# EMAIL_HOST = config('EMAIL_HOST')#'smtp.mailgun.org'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True
