from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Faculty, Department, Class, Subject 
from students.models import Student
from teacher.models import Teacher
from .forms import FacultyForm, DepartmentForm, ClassForm , SubjectForm
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q


def index(request):
    total_faculties = Faculty.objects.filter(is_deleted=False).count()
    total_departments = Department.objects.filter(is_deleted=False).count()
    total_students = Student.objects.filter(is_deleted=False).count()
    total_teachers = Teacher.objects.filter(is_deleted=False).count()
    teachers = Teacher.objects.filter(is_deleted=False)

    context = {
        'total_faculties': total_faculties,
        'total_departments': total_departments,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'teachers': teachers,
    }
    return render(request, 'academics/index.html', context)

def manage(request):
    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST)
        if faculty_form.is_valid():
            faculty_form.save()
            return redirect('manage')
    else:
        faculty_form = FacultyForm()
    
    return render(request, 'academics/manager.html', {'faculty_form': faculty_form})

def faculty_form(request):
    if request.method == 'POST':
        faculty_form = FacultyForm(request.POST)
        if faculty_form.is_valid():
            faculty_form.save()
            return redirect('manage')
    else:
        faculty_form = FacultyForm()
    
    return render(request, 'academics/faculty_form.html', {'faculty_form': faculty_form})

def department_form(request):
    if request.method == 'POST':
        department_form =  DepartmentForm(request.POST)
        if department_form.is_valid():
            department_form.save()
            return redirect('manage')
    else:
        department_form = DepartmentForm()
    return render(request, 'academics/department_form.html', {'department_form':department_form})

def class_form(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage')  # Başarıyla kaydedildikten sonra yönlendirme
    else:
        form = ClassForm()

    return render(request, 'academics/class_form.html', {'class_form': form})

def get_subjects(request):
    department_id = request.GET.get('department_id')
    if department_id:
        subjects = Subject.objects.filter(department_id=department_id)
        subjects_list = list(subjects.values('id', 'name'))
    else:
        subjects_list = []

    return JsonResponse({'subjects': subjects_list})

def subjects_form(request):
    if request.method == 'POST':
        subjects_form = SubjectForm(request.POST)
        if subjects_form.is_valid():
            subjects_form.save()
            return redirect('manage')  # 'manage' URL'sinin tanımlandığından emin olun
    else:
        subjects_form = SubjectForm()
    
    return render(request, 'academics/subjects_form.html', {'subjects_form': subjects_form})


class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculties/faculty_list.html'
    context_object_name = 'faculties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculties = Faculty.objects.filter(is_deleted=False)
        total_faculties = Faculty.objects.filter(is_deleted=False).count()
        total_departments = Department.objects.count()
        total_teachers = Teacher.objects.count()
        total_students = Student.objects.count()

        for faculty in faculties:
            faculty.department_count = Department.objects.filter(faculty=faculty).count()
            faculty.teacher_count = Teacher.objects.filter(department__faculty=faculty).count()
            faculty.student_count = Student.objects.filter(classroom__department__faculty=faculty).count()
            if total_departments > 0:
                faculty.department_percentage = (faculty.department_count / total_departments) * 100
            else:
                faculty.department_percentage = 0
            if total_teachers > 0:
                faculty.teacher_percentage = (faculty.teacher_count / total_teachers) * 100
            else:
                faculty.teacher_percentage = 0
            if total_students > 0:
                faculty.student_percentage = (faculty.student_count / total_students) * 100
            else:
                faculty.student_percentage = 0
        
        context['total_faculties'] = total_faculties
        context['total_departments'] = total_departments
        context['total_teachers'] = total_teachers
        context['total_students'] = total_students
        context['faculties'] = faculties
        return context
    
class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        queryset = Department.objects.filter(is_deleted=False).annotate(
            teacher_count=Count('teachers', filter=Q(teachers__is_deleted=False)),
            subject_count=Count('subjects', filter=Q(subjects__is_deleted=False))  # Eklenen alan
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_departments = Department.objects.filter(is_deleted=False).count()
        total_teachers = Teacher.objects.filter(is_deleted=False).count()
        total_students = Student.objects.filter(is_deleted=False).count()
        total_subjects = Subject.objects.filter(is_deleted=False).count()  # Doğru isimlendirme

        for department in context['departments']:
            # Öğrenci sayısını hesaplayalım
            department.student_count = Student.objects.filter(
                classroom__department=department, is_deleted=False
            ).count()
            
            # Öğretmen yüzdesini hesaplayalım
            if total_teachers > 0:
                department.teacher_percentage = (department.teacher_count / total_teachers) * 100
            else:
                department.teacher_percentage = 0
            
            # Öğrenci yüzdesini hesaplayalım
            if total_students > 0:
                department.student_percentage = (department.student_count / total_students) * 100
            else:
                department.student_percentage = 0

            # Konu yüzdesini hesaplayalım
            if total_subjects > 0:
                department.subject_percentage = (department.subject_count / total_subjects) * 100
            else:
                department.subject_percentage = 0

        context['total_departments'] = total_departments
        context['total_teachers'] = total_teachers
        context['total_students'] = total_students
        context['total_subjects'] = total_subjects  # Yazım hatası düzeltildi

        return context

        return context
class ClassListView(ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'  # Bu ismin HTML'de doğru kullanıldığından emin olun

    def get_queryset(self):
        return Class.objects.filter(is_deleted=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_classes'] = Class.objects.filter(is_deleted=False).count()
        return context
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
