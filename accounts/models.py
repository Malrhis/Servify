from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')

    def __str__(self):
        return self.name

class BusinessProfile(models.Model):
    """Service Provider specific profile"""
    business_name = models.CharField(max_length=255)
    business_description = models.TextField(blank=True)
    business_address = models.TextField(blank=True)
    business_website = models.URLField(blank=True)
    business_hours = models.JSONField(
        null=True, 
        blank=True,
        help_text=_("Store business hours in JSON format")
    )
    
    # Social media fields
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.business_name

class CustomerProfile(models.Model):
    """Customer specific profile"""
    delivery_address = models.TextField(
        blank=True,
        help_text=_("Primary delivery address")
    )
    preferred_communication = models.CharField(
        max_length=20,
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
            ('sms', _('SMS')),
        ],
        default='email'
    )

    def __str__(self):
        return f"Customer Profile for {self.user.email}"

class CustomUser(AbstractUser):
    """Custom user model for Servify."""
    roles = models.ManyToManyField(UserRole, blank=True)
    
    # Common fields
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Profile relationships
    business_profile = models.OneToOneField(
        BusinessProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user'
    )
    
    customer_profile = models.OneToOneField(
        CustomerProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user'
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.is_service_provider and self.business_profile:
            return f"{self.business_profile.business_name} ({self.email})"
        return self.email

    def get_full_name(self):
        if self.is_service_provider and self.business_profile:
            return self.business_profile.business_name
        return super().get_full_name() or self.email

    @property
    def is_service_provider(self):
        return self.roles.filter(name='service_provider').exists()

    @property
    def is_customer(self):
        return self.roles.filter(name='customer').exists()

    def add_role(self, role_name):
        role, _ = UserRole.objects.get_or_create(name=role_name)
        self.roles.add(role)
        if role_name == 'service_provider' and not self.business_profile:
            self.business_profile = BusinessProfile.objects.create()
        elif role_name == 'customer' and not self.customer_profile:
            self.customer_profile = CustomerProfile.objects.create()
        self.save()

    def remove_role(self, role_name):
        role = UserRole.objects.filter(name=role_name).first()
        if role:
            self.roles.remove(role)
            if role_name == 'service_provider':
                self.business_profile.delete()
                self.business_profile = None
            elif role_name == 'customer':
                self.customer_profile.delete()
                self.customer_profile = None
            self.save()

@receiver(post_save, sender=CustomUser)
def create_user_profiles(sender, instance, created, **kwargs):
    """Create profiles for new users based on their roles"""
    if created:
        # By default, all new users are customers
        instance.add_role('customer')
