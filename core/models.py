from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from bookings.models import Booking

class Review(models.Model):
    """Model for service reviews."""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    
    # Review visibility
    is_public = models.BooleanField(default=True)
    
    # Provider response
    provider_response = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.booking.service.name} by {self.reviewer.get_full_name()}"

class FAQ(models.Model):
    """Model for frequently asked questions."""
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['created_at']
    
    def __str__(self):
        return self.question
