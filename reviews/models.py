from django.db import models
from django.conf import settings
from listings.models import Listing
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Один отзыв на одно объявление от одного пользователя
        ordering = ['-created_at']  # Новые отзывы первыми (по желанию)

    def __str__(self):
        return f'Review by {self.user.username} for {self.listing.title}'


