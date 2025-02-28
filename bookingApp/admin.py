from django.contrib import admin
from .models import*

admin.site.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["room", "first_name", "last_name", "check_in", "check_out"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "price_per_night", "is_occupied"]    