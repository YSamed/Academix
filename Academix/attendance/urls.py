from django.urls import path
from .views import StartAttendanceView, ScanQRCodeView

urlpatterns = [
    path('start-attendance/', StartAttendanceView.as_view(), name='start-attendance'),
    path('scan-qr/', ScanQRCodeView.as_view(), name='scan-qr'),
]