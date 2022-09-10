from django.shortcuts import render

from rest_framework import serializers
from rest_framework.generics import ListAPIView

from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer