from django.contrib import admin

# Register your models here.

from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('original_id', 'original_title', 'rewritten_title', 'created_at')  # Fields to display in the list view
    search_fields = ('original_title', 'rewritten_title')  # Enable search functionality on these fields
    list_filter = ('created_at',)  # Add filter for 'created_at' field

admin.site.register(Property, PropertyAdmin)
