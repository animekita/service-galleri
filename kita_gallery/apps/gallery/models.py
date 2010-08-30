from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail.fields import ImageWithThumbnailsField

class CollectionGroup(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

class Collection(models.Model):
    slug = models.SlugField(unique=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    date = models.DateField()

    group = models.ForeignKey(CollectionGroup)

    @property
    def photographers(self):
        return Photographer.objects.filter(picture__collection=self).distinct()

    def __unicode__(self):
        return self.name

class Photographer(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Picture(models.Model):
    original = ImageWithThumbnailsField(
        upload_to='gallery-images/',
        thumbnail={'size': (600, 600)},
        extra_thumbnails={
            'small': {'size': (190, 190), 'options': ['crop', 'upscale']},
            },)

    caption = models.CharField(max_length=255, blank=True)

    collection = models.ForeignKey(Collection)
    photographer = models.ForeignKey(Photographer)

