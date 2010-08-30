from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.translation import ugettext as _

from sorl.thumbnail.fields import ImageWithThumbnailsField

class CollectionGroup(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

class Collection(models.Model):
    slug = models.SlugField(unique=True)

    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    date = models.DateField()

    group = models.ForeignKey(CollectionGroup)

    @property
    def photographers(self):
        return Photographer.objects.filter(picture__collection=self).distinct()

    def __unicode__(self):
        return self.name

class Photographer(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(_(u'Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.name

images_storage = FileSystemStorage(location=settings.IMAGES_ROOT,
                                   base_url=settings.IMAGES_URL)

class Picture(models.Model):
    def _get_upload_path(picture_obj, filename):
        collection_slug = picture_obj.collection.slug
        photographer_slug = picture_obj.photographer.slug

        return '%s/%s/%s' % (collection_slug, photographer_slug, filename)

    original = ImageWithThumbnailsField(
        upload_to=_get_upload_path,
        storage=images_storage,
        generate_on_save=True,
        thumbnail={'size': (600, 600)},
        extra_thumbnails={
            'small': {'size': (190, 190), 'options': ['crop', 'upscale']},
            },)

    caption = models.CharField(max_length=255, blank=True)

    collection = models.ForeignKey(Collection)
    photographer = models.ForeignKey(Photographer)

