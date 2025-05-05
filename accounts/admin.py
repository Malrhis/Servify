from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_service_provider', 'business_name']
    list_filter = UserAdmin.list_filter + ('is_service_provider',)
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {'fields': ('is_service_provider', 'business_name', 'business_description', 
                                          'profile_picture', 'phone_number', 'address', 'website')}),
        ('Social Media', {'fields': ('facebook', 'twitter', 'instagram', 'linkedin')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
