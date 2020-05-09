from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ArtistNames)
admin.site.register(models.TagsNames)
admin.site.register(models.Artwork)
admin.site.register(models.Category)