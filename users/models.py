from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('landlord', 'Landlord'),
        ('renter', 'Renter'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='renter')

    @property
    def is_landlord(self):
        return self.role == 'landlord'

    @property
    def is_renter(self):
        return self.role == 'renter'


