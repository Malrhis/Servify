from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from services.models import Service, ServiceAddon

class Booking(models.Model):
    """Model for service bookings."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    addons = models.ManyToManyField(ServiceAddon, blank=True, related_name='bookings')
    
    # Booking details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    number_of_participants = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Customer provided information
    special_requests = models.TextField(blank=True)
    
    # Payment information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_paid = models.BooleanField(default=False)
    fully_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Booking for {self.service.name} by {self.customer.get_full_name()}"
    
    def calculate_total_amount(self):
        """Calculate total amount including service price and addons."""
        total = self.service.price * self.number_of_participants
        for addon in self.addons.all():
            total += addon.price
        return total

class BookingNote(models.Model):
    """Notes associated with a booking."""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.booking} by {self.author.get_full_name()}"
