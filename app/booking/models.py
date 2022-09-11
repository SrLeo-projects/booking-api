from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    tv = models.BooleanField()
    air_conditioning = models.BooleanField()
    wifi = models.BooleanField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
    def is_available(self, check_in, check_out):
        check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
        
        bookings = self.booking_set.all()
        for booking in bookings:
            if booking.check_in <= check_out and booking.check_out >= check_in:
                return False
        return True

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        PAID = 'paid'
        CANCELED = 'canceled'
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    # Fecha de estadía
    check_in = models.DateField()
    check_out = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.room} - {self.user}'
    
    def get_amount(self):
        return self.room.price * (self.check_out - self.check_in).days

class Payment(models.Model):
    class Method(models.TextChoices):
        CREDIT_CARD = 'credit_card'
        DEBIT_CARD = 'debit_card'
        PAYPAL = 'paypal'
        BITCOIN = 'bitcoin'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    # Datos de facturación
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    # Monto y método de pago
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=11, choices=Method.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booking} - {self.amount}'