from django.contrib import admin
from attendance.models import QRCode, Attendance, StudentAttendance

# Register your models here.

admin.site.register(QRCode)
admin.site.register(Attendance)
admin.site.register(StudentAttendance)

