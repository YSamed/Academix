import base64
from io import BytesIO
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.views import View
from django.utils import timezone
from datetime import timedelta
import qrcode
import secrets
from attendance.forms import AttendanceForm
from attendance.models import QRCode, Attendance
from academics.models import Subject
from students.models import Student
from teacher.models import Teacher



class StartAttendanceView(View):
    
    def dispatch(self, request, *args, **kwargs):      
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.groups.filter(name='Yönetici').exists() or 
                request.user.groups.filter(name='Öğretmen').exists()):
            return HttpResponseForbidden("Bu Sayafaya Erişim İzniniz Yok")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            teacher = request.user.teacher
        except Teacher.DoesNotExist:
            return HttpResponseForbidden("Kullanıcı öğretmen değil.")
        
        form = AttendanceForm(teacher=teacher)
        subjects = teacher.subjects.all()
        
        context = {
            'form': form,
            'selected_teacher': teacher,
            'subjects': subjects,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'url': reverse('start-attendance'), 'name': 'Yoklama Sistemi'}
            ]
        }
        
        return render(request, 'attendance/start_attendance.html', context)

    def post(self, request, *args, **kwargs):
        try:
            teacher = request.user.teacher
        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Kullanıcı öğretmen değil.'}, status=403)
        
        form = AttendanceForm(request.POST, teacher=teacher)
        if form.is_valid():
            selected_subject_ids = form.cleaned_data['subject_ids']
            
            qr_code, qr_code_base64 = self.generate_qr_code_and_password(selected_subject_ids, teacher)
            
            subjects = Subject.objects.filter(id__in=selected_subject_ids)
            
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
        else:
            return JsonResponse({'error': 'Geçersiz form verisi.'}, status=400)

    def generate_qr_code_and_password(self, subjects, teacher):
        code = secrets.token_urlsafe(16)  # 16 karakterlik güvenli bir URL
        password = secrets.token_hex(3)  # 6 karakterlik bir şifre
        expires_at = timezone.now() + timedelta(seconds=10)

        qr_code = QRCode.objects.create(
            code=code,
            password=password,
            expires_at=expires_at,
            subject=subjects.first(),  # İlk dersi seçiyoruz
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
        img.save(buffered, 'PNG')  # PNG formatında kaydedin
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return qr_code, img_str


class ScanQRCodeView(View):
    def dispatch(self, request, *args, **kwargs):      
        # Yetkilendirme kontrolü
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.groups.filter(name='Yönetici').exists() or 
                request.user.groups.filter(name='Öğrenci').exists()):
            return HttpResponseForbidden("Bu Sayafaya Erişim İzniniz Yok")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)

        return render(request, 'attendance/scan_qr.html', {'student_id': student.id})

    def post(self, request, *args, **kwargs):
        qr_code_data = request.POST.get('qr_code')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')

        if not student_id:
            return JsonResponse({'status': 'student_id is required'}, status=400)

        student = get_object_or_404(Student, id=student_id)

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
