from django.contrib import admin
from .models import Review, FAQ

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'reviewer', 'rating', 'is_public', 'created_at']
    list_filter = ['rating', 'is_public', 'created_at']
    search_fields = ['comment', 'provider_response']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
