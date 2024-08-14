from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from students.models import Student
from .forms import StudentForm
from django.shortcuts import redirect

# Create your views here.

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(is_deleted=False)

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Öğrenci başarıyla kaydedildi .')
        return response

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Öğrenci başarıyla güncellendi.')
        return response

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        student.is_deleted = True
        student.save()
        messages.success(request, 'Öğrenci başarıyla silindi.')
        return redirect(self.success_url)



class StudentLoginView(LoginView):
    template_name = 'students/login.html'

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'student'):
                return reverse_lazy('index') 
            else:
                messages.error(self.request, "Öğrenci paneline giriş yapmak için öğrenci olmalısınız.")
                return reverse('students:login')
        return super().get_redirect_url()

        
class StudentLogoutView(LogoutView):
    next_page = reverse_lazy('students:login')