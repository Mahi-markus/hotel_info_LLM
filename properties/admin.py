from django.contrib import admin

# Register your models here.

from .models import Property,Summary,Description,RatingAndReview

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('original_id', 'original_title', 'rewritten_title', 'created_at')  # Fields to display in the list view
    search_fields = ('original_title', 'rewritten_title')  # Enable search functionality on these fields
    list_filter = ('created_at',)  # Add filter for 'created_at' field

admin.site.register(Property, PropertyAdmin)



@admin.register(Summary)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel_id', 'summary')

@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'description')   

@admin.register(RatingAndReview)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'rating','review')       