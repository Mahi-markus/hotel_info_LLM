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



class Description(models.Model):
    hotel_id = models.IntegerField()  # To associate the description with a specific hotel
    description = models.TextField(blank=True, null=True)  # Optional field for the description

    def __str__(self):
        return f"Description for Hotel ID: {self.hotel_id}"
    
class RatingAndReview(models.Model):
    hotel_id = models.CharField(max_length=255, unique=True)
    rating = models.FloatField()
    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'property_ratingandreview'
        verbose_name = "Rating and Review"
        verbose_name_plural = "Ratings and Reviews"

    def __str__(self):
        return f"{self.hotel_id} - Rating: {self.rating}"
