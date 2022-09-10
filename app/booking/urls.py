from django.urls import include, path

from booking import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='index'),
]