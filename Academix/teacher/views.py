from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.contrib.auth.views import LoginView, LogoutView
from teacher.models import Teacher
from teacher.forms import TeacherForm
from django.contrib import messages

# Create your views here.

class TeacherListViews(ListView):
    model = Teacher 
    template_name = 'teacher/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 7 

    def get_queryset(self):
        return Teacher.objects.filter(is_deleted=False)
    

class TeacherDetailViews(DetailView):
    model = Teacher
    template_name = 'teacher/taecher_detail.html'
    context_object_name = 'teaacher'


class TeacherCreateViews(CreateView):
    name = Teacher
    form_class = TeacherForm
    template_name ='teacher/teacher_form.html'
    success_url = reverse_lazy('teacher-list')

    def form_valid(self , form):
        response = super().form_valid(form)
        messages.success(self.request,'Öğretmen başarıyla oluşturuldu.')
        return response


class TeacehrUpdateViews(UpdateView):
    model = Teacher
    template_name = 'teacher/tae'
    success_url = reverse_lazy('')

    def post(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.is_deleted = True
        teacher.save()
        messages.success(request, 'Öğretmen başarıyla silindi.')
        return redirect(self.success_url)


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.is_deleted = True
    teacher.save()
    messages.success(request, f"{teacher.first_name} {teacher.last_name} başarıyla silindi.")
    return redirect(reverse('teachers:teacher-list'))


class TeacherLoginView(LoginView):
    template_name = 'teacher/login.html'

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'teacher'):
                return reverse_lazy('index') 
            else:
                messages.error(self.request, "Öğretmen paneline giriş yapmak için öğretmen olmalısınız.")
                return reverse_lazy('teachers:login')  
        return super().get_redirect_url()
      
class TeacherLogoutView(LogoutView):
    next_page = reverse_lazy('index')