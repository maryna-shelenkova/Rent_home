from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'listing__title')
