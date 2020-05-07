from django.db import models
from artworkpage.models import Artwork


# Contains information about display categories, category is a chosen group of tags which is advertised with a banner.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    associated_artworks = models.ManyToManyField(Artwork)
    associated_tags = models.CharField(default="", max_length=128)
    priority_level = models.PositiveIntegerField(default=3)  # Scale of 1-10 probably
    banner_artwork = models.ImageField(upload_to="banner")
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
