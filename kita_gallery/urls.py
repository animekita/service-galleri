from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',)

admin.autodiscover()

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns('',
        (r'^gallery-images/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.IMAGES_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('kita_gallery.apps.gallery.urls')),
)