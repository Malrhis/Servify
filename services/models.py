from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class ServiceCategory(models.Model):
    """Categories for services (e.g., Consulting, Teaching, Repair)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Service Categories"
    
    def __str__(self):
        return self.name

class Service(models.Model):
    """Model for individual services offered by service providers."""
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    deposit_required = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Service availability
    is_active = models.BooleanField(default=True)
    max_participants = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Service images
    featured_image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} by {self.provider.get_full_name()}"

class ServiceAddon(models.Model):
    """Additional options that can be added to a service."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_minutes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.name} for {self.service.name}"
