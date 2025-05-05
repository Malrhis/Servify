from django.contrib import admin
from .models import ServiceCategory, Service, ServiceAddon

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class ServiceAddonInline(admin.TabularInline):
    model = ServiceAddon
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'category', 'price', 'is_active']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'provider__username']
    inlines = [ServiceAddonInline]
