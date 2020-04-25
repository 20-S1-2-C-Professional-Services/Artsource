from django.db import models
from user.models import User


# Create your models here.
class Artwork(models.Model):
    """Artwork table"""

    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to='Img')
    thumbnail = models.ImageField(upload_to='Thumbnail')
    user = models.ForeignKey(User, related_name='artwork_user', on_delete=models.CASCADE)
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

