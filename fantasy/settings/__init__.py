from decouple import config

if config('SERVER') == 'development':
    from .development import *
elif config('SERVER') == 'production':
    from .production import *
elif config('SERVER') == 'testing':
    from .testing import *
else:
    from .base import *
