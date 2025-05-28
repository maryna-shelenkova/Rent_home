from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('landlord', 'Landlord'),
        ('renter', 'Renter'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    @property
    def is_landlord(self):
        return self.role == 'landlord'

    @property
    def is_renter(self):
        return self.role == 'renter'

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username

