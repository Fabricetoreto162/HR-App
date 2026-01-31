from django.urls import path
from .views import CheckInView, CheckOutView

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='check-in'),
    path('check-out/', CheckOutView.as_view(), name='check-out'),
]