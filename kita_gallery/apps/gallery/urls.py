from django.conf.urls.defaults import *

urlpatterns = patterns('kita_gallery.apps.gallery.views',
    url(r'^management/nyt-event/', 'create_collection',
        name='gallery_create_collection'),

    url(r'^management/ny-fotograf/', 'create_photographer',
        name='gallery_create_photographer'),

    url(r'^management/rediger-event/([0-9]+)/', 'edit_collection',
        name='gallery_edit_collection'),

    url(r'^management/rediger-fotograf/([0-9]+)/', 'edit_photographer',
        name='gallery_edit_photographer'),

    url(r'^management/rediger-billede/([0-9]+)/', 'edit_picture',
        name='gallery_edit_picture'),

    url(r'^management/upload/([0-9]+)/([0-9]+)/callback/', 'upload_images_callback',
        name='gallery_upload_images_callback'),

    url(r'^management/upload/([0-9]+)/([0-9]+)/', 'upload_images_step2',
        name='gallery_upload_images_step2'),

    url(r'^management/upload/', 'upload_images_step1',
        name='gallery_upload_images'),

    url(r'^event/([0-9]+)/([0-9]+)/', 'view_collection',
        name='gallery_view_collection'),
    url(r'^event/([0-9]+)/', 'view_collection',
        name='gallery_view_collection'),

    url(r'^picture/([0-9]+)/', 'view_picture', name='gallery_view_picture'),
    url(r'^', 'list_collections', name='gallery_list_collections'),
)