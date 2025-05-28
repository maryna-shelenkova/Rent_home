from django.db import models
from django.conf import settings
from listings.models import Listing



class Booking(models.Model):
    # Ссылка на пользователя, который сделал бронирование
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')

    # Ссылка на объявление, которое бронируется
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')

    # Дата начала и окончания бронирования
    start_date = models.DateField()
    end_date = models.DateField()

    # Статус бронирования
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # В ожидании
        ('confirmed', 'Confirmed'),  # Подтверждено арендодателем
        ('cancelled', 'Cancelled'),  # Отменено
        ('declined', 'Declined'),  # Отклонено арендодателем
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user} for {self.listing}'

