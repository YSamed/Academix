import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
import qrcode
import secrets
from attendance.models import QRCode, Attendance
from academics.models import Class, Department, Faculty
from students.models import Student
from teacher.models import Teacher

class StartAttendanceView(View):
    def get(self, request, *args, **kwargs):
        course = self.get_default_course()
        teachers = Teacher.objects.all()  # Tüm öğretmenleri listele
        return render(request, 'attendance/start_attendance.html', {'course': course, 'teachers': teachers})

    def post(self, request, *args, **kwargs):
        course = self.get_default_course()
        teacher_id = request.POST.get('teacher_id')  # Öğretmen ID'sini formdan al
        teacher = get_object_or_404(Teacher, id=teacher_id)  # Öğretmeni al
        qr_code, qr_code_base64 = self.generate_qr_code_and_password(course, teacher)
        
        subjects = teacher.subjects.all()  # Öğretmenin derslerini al
        
        response_data = {
            'qr_code': qr_code_base64,
            'password': qr_code.password,
            'teacher': {
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
            },
            'subjects': list(subjects.values('name'))
        }

        return JsonResponse(response_data)

    def generate_qr_code_and_password(self, course, teacher):
        code = secrets.token_urlsafe(16)  # 16 karakterlik güvenli bir URL
        password = secrets.token_hex(3)  # 6 karakterlik bir şifre 
        expires_at = timezone.now() + timedelta(seconds=10)

        qr_code = QRCode.objects.create(
            code=code,
            password=password,
            expires_at=expires_at,
            course=course,
            teacher=teacher
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return qr_code, img_str

    def get_default_course(self):
        # Varsayılan bir fakülte oluştur veya al
        default_faculty, created = Faculty.objects.get_or_create(name='Varsayılan Fakülte')

        # Varsayılan bir bölüm oluştur veya al
        default_department, created = Department.objects.get_or_create(name='Varsayılan Bölüm', faculty=default_faculty)

        # Varsayılan kursu al veya oluştur ve varsayılan bölümü ata
        default_course, created = Class.objects.get_or_create(name='Varsayılan Kurs', defaults={'department': default_department})
        return default_course


class ScanQRCodeView(View):
    def get(self, request, *args, **kwargs):
        students = Student.objects.filter(is_deleted=False)
        return render(request, 'attendance/scan_qr.html', {'students': students})

    def post(self, request, *args, **kwargs):
        qr_code_data = request.POST.get('qr_code')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')

        # Öğrenci ID'sinin olup olmadığını kontrol et
        if not student_id:
            return JsonResponse({'status': 'student_id is required'}, status=400)

        student = get_object_or_404(Student, id=student_id)

        # QR kodu veya şifre kontrolü
        if qr_code_data:
            try:
                qr_code = QRCode.objects.get(code=qr_code_data)
                if qr_code.is_valid() and (password == qr_code.password or not password):
                    Attendance.objects.create(student=student, qr_code=qr_code)
                    qr_code.is_active = False
                    qr_code.save()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'invalid or expired QR code or incorrect password'}, status=400)
            except QRCode.DoesNotExist:
                return JsonResponse({'status': 'invalid QR code'}, status=400)
        
        if password:
            try:
                qr_code = QRCode.objects.get(password=password)
                if qr_code.is_valid():
                    Attendance.objects.create(student=student, qr_code=qr_code)
                    qr_code.is_active = False
                    qr_code.save()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'invalid or expired QR code or incorrect password'}, status=400)
            except QRCode.DoesNotExist:
                return JsonResponse({'status': 'invalid password'}, status=400)
        
        return JsonResponse({'status': 'qr_code or password is required'}, status=400)
