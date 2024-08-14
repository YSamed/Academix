from django.db import models
from django.utils import timezone
from academics.models import Class , Subject
from students.models import Student
from teacher.models import Teacher

# Create your models here.


class QRCode(models.Model):
    code = models.CharField(max_length=256)  # QR kodunun verisi
    password = models.CharField(max_length=6)  # 6 haneli şifre
    expires_at = models.DateTimeField()  # QR kodunun geçerlilik süresi
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='qr_codes')  

    def __str__(self):
        course_name = self.subject.name if self.subject else 'No Course'
        teacher_name = f"{self.teacher.first_name} {self.teacher.last_name}" if self.teacher else 'No Teacher'
        return f"{course_name} - {teacher_name}"



    def is_valid(self):
        """ QR kodunun geçerli olup olmadığını kontrol eder. """
        return self.is_active and self.expires_at > timezone.now()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')  
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='attendances') 
    timestamp = models.DateTimeField(auto_now_add=True)  # Yoklama zamanını otomatik olarak ekler

    def __str__(self):
        return f'{self.student} - {self.qr_code} - {self.timestamp}'
    


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendances')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='student_attendances')
    date = models.DateField()  # Yoklamanın yapıldığı tarih
    is_present = models.BooleanField(default=False)  # Öğrencinin derste olup olmadığı

    class Meta:
        unique_together = ('student', 'class_instance', 'date')