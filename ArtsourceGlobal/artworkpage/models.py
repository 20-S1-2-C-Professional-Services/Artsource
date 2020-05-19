from django.db import models
from user.models import User


class ArtistNames(models.Model):
    """just used for store the name different tags"""
    artist_names = models.CharField(max_length=128)
    objects = models.Manager()


class TagsNames(models.Model):
    """just used for store the name different tags"""

    tag_names = models.CharField(max_length=128, unique=True)
    objects = models.Manager()


# Create your models here.
class Artwork(models.Model):
    """Artwork table"""

    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='Img')
    thumbnail = models.ImageField(upload_to='Thumbnail')
    user = models.ForeignKey(User, related_name='artwork_user', on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    booked = models.BooleanField(default=False)
    tags = models.CharField(max_length=128, default='')
    # add() and remove() for this manytomany field, clear() is remove all
    artists = models.ManyToManyField(ArtistNames, related_name='created_artwork')
    artists_string = models.CharField(max_length=512,default='')
    description = models.CharField(max_length=512, default='')
    height = models.FloatField(default=0)
    width = models.FloatField(default=0)
    length = models.FloatField(default=0)
    objects = models.Manager()

    # url_height = models.PositiveIntegerField(default=75)
    # url_width = models.PositiveIntegerField(default=75)
    # image = models.ImageField(upload_to="Img", height_field='url_height', width_field='url_width')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'artwork'
        verbose_name_plural = 'artworks'


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)
    tags_list = models.CharField(max_length=128)
    artwork_name_list = models.CharField(max_length=512)
    artwork_list = models.ManyToManyField(Artwork, related_name='artwork_category')
    banner = models.ImageField(upload_to='banner')
    objects = models.Manager()
