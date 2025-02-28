from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    full_name = models.CharField(max_length=50, default="Unknown Guest")
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    card_holder = models.CharField(max_length=40, default="Unknown")
    card_number = models.IntegerField(null=True, blank=True, default=0)
    exp_month = models.IntegerField(null=True, blank=True, default=1)
    exp_year =models.IntegerField(null=True, blank=True, default=2030)
    cvv = models.IntegerField(null=True, blank=True, default=000)
    total_price = models.DecimalField(max_digits = 10, decimal_places=2, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.full_name} - {self.room.name}"
