from django.contrib import admin
from . import models

# register the db tables in admin site
admin.site.register(models.User)
admin.site.register(models.EmailVerifyRecord)
