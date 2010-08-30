from django.conf.urls.defaults import *

SLUG = '[a-zA-Z\-_0-9]+'

urlpatterns = patterns('kita_gallery.apps.gallery.views',

    # collection

    url(r'^arrangement/ny/',
        'create_collection',
        name='gallery_create_collection'),

    url(r'^arrangement/(?P<collection_slug>%s)/rediger/' % SLUG,
        'edit_collection',
        name='gallery_edit_collection'),

    url(r'^arrangement/(?P<collection_slug>%s)/upload/(?P<photographer_slug>%s)/callback/' % (SLUG, SLUG),
        'upload_images_callback',
        name='gallery_upload_images_callback'),

    url(r'^arrangement/(?P<collection_slug>%s)/upload/(?P<photographer_slug>%s)/' % (SLUG, SLUG),
        'upload_images_step2',
        name='gallery_upload_images_step2'),

    url(r'^arrangement/(?P<collection_slug>%s)/upload/' % SLUG,
        'upload_images_step1',
        name='gallery_upload_images'),


    url(r'^arrangement/(?P<collection_slug>%s)/billede/(?P<picture_id>[0-9]+)/' % SLUG,
        'view_collection_picture',
        name='gallery_view_collection_picture'),

    url(r'^arrangement/(?P<collection_slug>%s)/side/(?P<page_number>[0-9]+)/' % SLUG,
        'view_collection',
        name='gallery_view_collection'),

    url(r'^arrangement/(?P<collection_slug>%s)/' % SLUG,
        'view_collection',
        name='gallery_view_collection'),

    # photographer

    url(r'^fotograf/ny/',
        'create_photographer',
        name='gallery_create_photographer'),

    url(r'^fotograf/(?P<photographer_slug>%s)/rediger/' % SLUG,
        'edit_photographer',
        name='gallery_edit_photographer'),

    url(r'^fotograf/(?P<collection_slug>%s)/billede/(?P<picture_id>[0-9]+)/' % SLUG,
        'view_photographer_picture',
        name='gallery_view_photographer_picture'),

    url(r'^fotograf/(?P<collection_slug>%s)/side/(?P<page_number>[0-9]+)/' % SLUG,
        'view_photographer',
        name='gallery_view_photographer'),

    url(r'^fotograf/(?P<collection_slug>%s)/' % SLUG,
        'view_photographer',
        name='gallery_view_photographer'),

    # other

    url(r'^', 'list_collections', name='gallery_list_collections'),
)