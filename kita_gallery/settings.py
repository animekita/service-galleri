# Django settings for kita_gallery project.

import os
DIRNAME = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kita_gallery',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

TIME_ZONE = 'Europe/Copenhagen'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_URL = 'http://alpha.kita.dk:8000'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/semadk/src/kita-svn/static/trunk/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://alpha.kita.dk:8000/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l0m$ijxnn-w*+xkpe9x8e%e7aakk#6w*@wl3d6^-vu1shtumv2'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'selvbetjening-sso.middleware.SelvbetjeningUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'selvbetjening.context_processors.site_urls',

    'django.core.context_processors.media',
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',

    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'kita_gallery.urls'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    'crumbs',
    'sorl.thumbnail',
    'uni_form',

    'selvbetjening.viewhelpers.googleanalytics',
    'selvbetjening.viewhelpers.copyright',

    'kita_gallery.apps.gallery',
)

AUTHENTICATION_BACKENDS = ('kita_gallery.apps.gallery.backends.PhotographerPermissionBackend',
                           'selvbetjening-sso.backends.SelvbetjeningBackend',
                           'django.contrib.auth.backends.ModelBackend')

SAPI_AUTH_TOKEN_KEY = 'kita_auth_token'
SAPI_SERVICE_ID = 'test'
SAPI_URL = 'http://alpha.kita.dk:8001'