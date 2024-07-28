from datetime import timezone
from django.test import TestCase

# Create your tests here.


# tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from Academix.attendance.views import generate_qr_code_and_password
from academics.models import Class
from students.models import Student
from teacher.models import Teacher
from .models import QRCode, Attendance

class QRCodeTests(TestCase):

    def setUp(self):
        # Öğretmen ve öğrenci oluştur
        self.teacher = Teacher.objects.create(first_name='John', last_name='Doe', employee_id='T123')
        self.course = Class.objects.create(name='Math 101', faculty=self.teacher)
        self.student = Student.objects.create(first_name='Jane', last_name='Smith', student_id='S456', classroom=self.course)

        # Kullanıcı oluştur
        self.user = User.objects.create_user(username='student1', password='password123')
        self.user.student = self.student
        self.user.save()

    def test_generate_qr_code_and_password(self):
        qr_code = generate_qr_code_and_password(self.course, self.teacher)
        
        self.assertTrue(QRCode.objects.filter(code=qr_code.code, password=qr_code.password).exists())
        self.assertEqual(qr_code.course, self.course)
        self.assertEqual(qr_code.teacher, self.teacher)
        self.assertTrue(qr_code.expires_at > timezone.now())

    def test_scan_qr_code_success(self):
        qr_code = generate_qr_code_and_password(self.course, self.teacher)
        
        response = self.client.post('/scan_qr_code/', {'qr_code': qr_code.code, 'password': qr_code.password}, HTTP_AUTHORIZATION='Token <TOKEN>')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(Attendance.objects.filter(student=self.student, qr_code=qr_code).exists())

    def test_scan_qr_code_failure(self):
        qr_code = generate_qr_code_and_password(self.course, self.teacher)
        
        # Test invalid or expired QR code
        response = self.client.post('/scan_qr_code/', {'qr_code': qr_code.code, 'password': 'wrongpassword'}, HTTP_AUTHORIZATION='Token <TOKEN>')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'invalid or expired')
