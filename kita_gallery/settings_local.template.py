# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STATIC_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Selvbetjening API Settings
SAPI_AUTH_TOKEN_KEY = 'kita_auth_token'
SAPI_SERVICE_ID = 'gallery'
SAPI_URL = 'http://alpha.kita.dk:8001'

# Site URL Settings
SITE_URL = 'http://alpha.kita.dk:8000' # without trailing slash
MEDIA_URL = 'http://alpha.kita.dk:8000/static/' # with trailing slash
ADMIN_MEDIA_PREFIX = '/media/' # with trailing slash

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/home/semadk/src/kita-svn/static/trunk/' # with trailing slash

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kita_gallery',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

