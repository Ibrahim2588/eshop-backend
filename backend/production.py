from .settings import *

import dj_database_url


DEBUG = False
TEMPLATE_DEBUG = False


SECRET_KEY = 'k3$m2^e%@$f!nb@=i2qzmrybe%oag!(&3e3o8d(!7@&o8g0=df'


DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = [
    'shopbackend258.herokuapp.com',
]
