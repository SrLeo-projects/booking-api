from django.urls import include, path

from booking import views

app_name = 'booking'

urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/bookings/', views.BookedRoomView.as_view(), name='room-bookings'),

    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/pay/', views.PaymentCreateView.as_view(), name='booking-pay')
]