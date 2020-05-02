from django.db import models
from user.models import User
from homepage.models import Artwork
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from user.models import User
from artworkpage.models import Artwork


# Create a Reservation Model which stores booking details
class Reservation(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, related_name='artwork', on_delete=models.CASCADE)
    renter = models.ForeignKey(User, related_name='renter', on_delete=models.CASCADE)
    CheckIn = models.DateField()
    CheckOut = models.DateField()
    totalPrice = models.IntegerField(default=0)
    objects = models.Manager()

    def get_id(self):
        return self.id

    def get_checkin(self):
        return self.CheckIn

    def get_checkout(self):
        return self.CheckOut

    class Meta:
        verbose_name_plural = 'Reservation'

    def __str__(self):
        return self.owner
