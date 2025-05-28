from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'price', 'rooms', 'property_type', 'is_active', 'owner')
    search_fields = ('title', 'description', 'location')
    list_filter = ('property_type', 'is_active', 'rooms')
    list_editable = ('is_active',)
