from django.db import models

# Create your models here.
# property_info/models.py


class Property(models.Model):
    original_id = models.IntegerField()  # To reference the original ecommerce property
    original_title = models.CharField(max_length=255)
    rewritten_title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rewritten_properties'
        
    def __str__(self):
        return f"{self.original_title} -> {self.rewritten_title}"
    



class Summary(models.Model):
    hotel_id = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return f"Summary for Hotel ID: {self.hotel_id}"
