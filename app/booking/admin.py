from django.contrib import admin

from booking.models import *

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'tv', 'air_conditioning', 'wifi', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'room', 'user')
    search_fields = ('room__name', 'user__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'name', 'last_name', 'email', 'amount', 'method')
    list_filter = ('booking__status', 'booking__room', 'booking__user')
    search_fields = ('booking__room__name', 'booking__user__username')