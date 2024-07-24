from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from teacher.models import Teacher
from teacher.forms import TeacherForm
from django.contrib import messages

# Create your views here.


class TeacherListViews(ListView):
    model = Teacher 
    template_name = 'teacher/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return Teacher.objects.filter(is_deleted=False)
    

class TeacherDetailViews(DeleteView):
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


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher-list')

    def post(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.is_deleted = True
        teacher.save()
        messages.success(request, 'Öğretmen başarıyla silindi.')
        return redirect(self.success_url)