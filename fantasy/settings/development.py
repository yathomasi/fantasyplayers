from .base import *

# DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEBUG_TOOLBAR_CONFIG = {
#     # 'JQUERY_URL': '',
#     "SHOW_TOOLBAR_CALLBACK": config('SHOW_DEBUG_TOOLBAR'),

# }
INTERNAL_IPS = '127.0.0.1'
