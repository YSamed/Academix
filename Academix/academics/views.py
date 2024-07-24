from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Faculty, Department, Class
from .forms import FacultyForm, DepartmentForm, ClassForm

# Listeleme View'ları
class FacultyListView(ListView):
    model = Faculty
    template_name = 'academics/faculty_list.html'
    context_object_name = 'faculties'

    def get_queryset(self):
        return Faculty.objects.filter(is_deleted=False)

class DepartmentListView(ListView):
    model = Department
    template_name = 'academics/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.filter(is_deleted=False)

class ClassListView(ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(is_deleted=False)

# Detay View'ları
class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'academics/faculty_detail.html'
    context_object_name = 'faculty'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()
        context['departments'] = faculty.departments.filter(is_deleted=False)
        return context

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'academics/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['classes'] = department.classes.filter(is_deleted=False)
        return context

class ClassDetailView(DetailView):
    model = Class
    template_name = 'academics/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sınıfa ait öğrencileri al
        class_instance = self.get_object()
        context['students'] = class_instance.students.filter(is_deleted=False)
        # Sınıfa ait dersleri al
        context['subjects'] = class_instance.subjects.filter(is_deleted=False)
        return context

# Güncelleme View'ları
class FacultyUpdateView(UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'academics/faculty_form.html'
    success_url = reverse_lazy('faculty-list')

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/department_form.html'
    
    def get_success_url(self):
        return reverse_lazy('faculty-detail', kwargs={'pk': self.object.faculty.pk})

class ClassUpdateView(UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'academics/class_form.html'

    def get_success_url(self):
        # Burada 'department-detail' URL'sine yönlendirmek istiyorsanız, doğru PK'yi sağlamalısınız.
        # Örneğin, sınıfın bağlı olduğu bölümün detayına yönlendirebiliriz:
        return reverse_lazy('department-detail', kwargs={'pk': self.object.department.pk})

# Silme View'ları
class FacultyDeleteView(DeleteView):
    model = Faculty
    template_name = 'academics/faculty_confirm_delete.html'
    success_url = reverse_lazy('faculty-list')

    def post(self, request, *args, **kwargs):
        faculty = self.get_object()
        faculty.is_deleted = True
        faculty.save()
        return redirect(self.success_url)

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'academics/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')

    def post(self, request, *args, **kwargs):
        department = self.get_object()
        department.is_deleted = True
        department.save()
        return redirect(self.success_url)

class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'academics/class_confirm_delete.html'
    success_url = reverse_lazy('class-list')

    def post(self, request, *args, **kwargs):
        class_ = self.get_object()
        class_.is_deleted = True
        class_.save()
        return redirect(self.success_url)

# Yönetim View'ı
def manage_academics(request):
    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST, prefix='faculty')
        department_form = DepartmentForm(request.POST, prefix='department')
        class_form = ClassForm(request.POST, prefix='class')

        if faculty_form.is_valid():
            faculty_form.save()
        if department_form.is_valid():
            department_form.save()
        if class_form.is_valid():
            class_form.save()

        return redirect('manage-academics')
    else:
        faculty_form = FacultyForm(prefix='faculty')
        department_form = DepartmentForm(prefix='department')
        class_form = ClassForm(prefix='class')

    return render(request, 'academics/manage_academics.html', {
        'faculty_form': faculty_form,
        'department_form': department_form,
        'class_form': class_form,
    })
