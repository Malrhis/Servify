from django.contrib import admin
from .models import Booking, BookingNote

class BookingNoteInline(admin.TabularInline):
    model = BookingNote
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['service', 'customer', 'start_time', 'status', 'total_amount', 'fully_paid']
    list_filter = ['status', 'deposit_paid', 'fully_paid', 'created_at']
    search_fields = ['service__name', 'customer__username', 'special_requests']
    inlines = [BookingNoteInline]
