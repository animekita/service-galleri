# Django settings for kita_gallery project.

import os
DIRNAME = os.path.abspath(os.path.dirname(__file__))

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

    'kita_gallery.apps.gallery',
)

AUTHENTICATION_BACKENDS = ('kita_gallery.apps.gallery.backends.PhotographerPermissionBackend',
                           'selvbetjening-sso.backends.SelvbetjeningBackend',
                           'django.contrib.auth.backends.ModelBackend')

# other settings
ROOT_URLCONF = 'kita_gallery.urls'

# import localsettings, a per deployment configuration file
try:
    from settings_local import *
except ImportError:
    pass
