from datetime import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from booking.serializers import PaymentCreateSerializer, RoomSerializer, BookingSerializer, BookingCreateSerializer
from booking.models import Payment, Room, Booking

'''
Al ingresar al sitio web se deben mostrar todas las habitaciones disponibles
Dbe tener la posibilidad de filtrar por capacidad, tv, aire acondicionado, wifi y precio
'''
class RoomListView(ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        filters = ['capacity', 'tv', 'air_conditioning', 'wifi', 'price']
        for filter in filters:
            if self.request.GET.get(filter):
                queryset = queryset.filter(**{filter: self.request.GET.get(filter)})
        return queryset

# El usuario debe poder revisar el detalle de una habitación
class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'

# Se debe restringir la selección de fechas según las reservas pendientes o pagadas
class BookedRoomView(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        room_id = self.kwargs['pk']
        queryset = queryset.filter(room_id=room_id, status__in=[Booking.Status.PENDING, Booking.Status.PAID])
        return queryset

# Para realizar una reserva debe ser un usuario registrado y el listado solo debe mostrar las reservaciones del mismo
class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookingSerializer
        return BookingCreateSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        check_in = request.data['check_in']

        if datetime.strptime(check_in, '%Y-%m-%d').date() < datetime.today().date():
            return Response({"error": "Cannot book a room in the past"}, status=status.HTTP_400_BAD_REQUEST)
        
        check_out = request.data['check_out']
        
        if check_out < check_in:
            return Response({'error': 'check_out must be greater than check_in'}, status=status.HTTP_400_BAD_REQUEST)

        room_id = request.data['room']
        room = get_object_or_404(Room, pk=room_id)
        
        if not room.is_available(check_in, check_out):
            return Response({'error': 'The room is not available'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

# El usuario podrá ver el detalle de la reserva que va a realizar antes de realizar el pago
class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'

'''
Se considerará la integración de la Pasarela de Pagos como externa
Se debe esperar un POST con los datos del pago
'''
class PaymentCreateView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer

    def create(self, request, *args, **kwargs):
        booking_id = request.data['booking']
        booking = get_object_or_404(Booking, pk=booking_id)
        if booking.status != Booking.Status.PENDING:
            return Response({'error': 'The booking is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.Status.PAID
        booking.save()
        return super().create(request, *args, **kwargs)