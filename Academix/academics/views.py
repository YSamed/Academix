from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView ,CreateView
from django.urls import reverse, reverse_lazy
from django.http import  JsonResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Faculty, Department, Class, Subject
from students.models import Student
from teacher.models import Teacher
from .forms import FacultyForm, DepartmentForm, ClassForm, SubjectForm ,ClassSubjectForm


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

def faculty_form(request, pk=None):
    if pk:
        # Düzenleme işlemi için mevcut faculty nesnesini al
        faculty = get_object_or_404(Faculty, pk=pk)
        if request.method == 'POST':
            form = FacultyForm(request.POST, instance=faculty)
            if form.is_valid():
                form.save()
                return redirect('manage')
        else:
            form = FacultyForm(instance=faculty)
    else:
        # Yeni faculty ekleme işlemi
        if request.method == 'POST':
            form = FacultyForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage')
        else:
            form = FacultyForm()
    
    return render(request, 'academics/faculty_form.html', {'form': form})

def department_form(request, faculty_id=None):
    if request.method == 'POST':
        department_form = DepartmentForm(request.POST, faculty_id=faculty_id)
        if department_form.is_valid():
            department = department_form.save(commit=False)
            if faculty_id:
                faculty = get_object_or_404(Faculty, id=faculty_id)
                department.faculty = faculty
            department.save()
            return redirect('manage')
    else:
        # GET isteği ise
        department_form = DepartmentForm(faculty_id=faculty_id)

    return render(request, 'academics/department_form.html', {'department_form': department_form})

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

def delete_department(request, pk ):
    department = get_object_or_404(Department , pk = pk)
    department.is_deleted = True
    department.save()
    messages.success(request, f"{department.name} başarıyla silindi.")

    return redirect(reverse ('faculty-detail',kwargs={'pk':department.faculty.pk}))


# Ekleme 
class AddSubjectView(CreateView):
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['class_id'] = self.kwargs.get('class_id', None)  # class_id'yi formun kwargs'ına ekleyin
        return kwargs

    def form_valid(self, form):
        # Formu kaydedin
        SubjectForm = form.save()
        
        # class_id parametresini URL'den al
        class_id = self.kwargs.get('class_id', None)
        
        # class_id varsa, detay sayfasına yönlendir
        if class_id:
            return redirect('class_detail', pk=class_id)
        
        # class_id yoksa, başka bir URL'ye yönlendirin
        return redirect('manage')

# academics/views.py

from django.urls import reverse

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/department_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        faculty_id = self.kwargs.get('faculty_id')
        if faculty_id:
            kwargs['faculty_id'] = faculty_id
        return kwargs

    def form_valid(self, form):
        faculty_id = self.kwargs.get('faculty_id')
        if faculty_id:
            form.instance.faculty_id = faculty_id
        return super().form_valid(form)

    def get_success_url(self):
        faculty_id = self.kwargs.get('faculty_id')
        if faculty_id:
            # Fakülte detay sayfasına yönlendir ÇALIŞMIYOR
            return reverse('faculty-detail', kwargs={'pk': faculty_id})
        return reverse('department-list')  # Fakülte ID'si yoksa departman listesine yönlendir


# Listeleme 
class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculties/faculty_list.html'
    context_object_name = 'faculties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculties = Faculty.objects.filter(is_deleted=False)
        total_faculties = faculties.count()
        total_departments = Department.objects.filter(is_deleted=False).count()
        total_teachers = Teacher.objects.filter(is_deleted=False).count()
        total_students = Student.objects.filter(is_deleted=False).count()

        for faculty in faculties:
            faculty.department_count = Department.objects.filter(faculty=faculty, is_deleted=False).count()
            faculty.teacher_count = Teacher.objects.filter(department__faculty=faculty, is_deleted=False).count()
            faculty.student_count = Student.objects.filter(classroom__department__faculty=faculty, is_deleted=False).count()
            faculty.department_percentage = (faculty.department_count / total_departments) * 100 if total_departments > 0 else 0
            faculty.teacher_percentage = (faculty.teacher_count / total_teachers) * 100 if total_teachers > 0 else 0
            faculty.student_percentage = (faculty.student_count / total_students) * 100 if total_students > 0 else 0
        
        context.update({
            'total_faculties': total_faculties,
            'total_departments': total_departments,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'faculties': faculties
        })
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
        total_subjects = Subject.objects.filter(is_deleted=False).count()  


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
        context['total_subjects'] = total_subjects 

        return context

class ClassListView(ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'  

    def get_queryset(self):
        return Class.objects.filter(is_deleted=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_classes'] = Class.objects.filter(is_deleted=False).count()
        return context







# Detay
# academics/views.py

class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'academics/faculty_detail.html'
    context_object_name = 'faculty'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()
        
        # Fetch departments
        departments = faculty.departments.filter(is_deleted=False)
        departments_count = departments.count()
        faculty_students_count = Student.objects.filter(classroom__department__in=departments, is_deleted=False).count()
        faculties_teachers_count = Teacher.objects.filter(department__in=departments, is_deleted=False).count()
        
        # Pagination
        paginator = Paginator(departments, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Prepare data
        departments_with_classes = []
        for department in page_obj:
            classes = department.classes.filter(is_deleted=False).order_by('name')
            classes_with_students_count = classes.annotate(total_students=Count('students'))
            departments_with_classes.append({
                'department': department,
                'classes': classes_with_students_count
            })

        context.update({
            'departments_with_classes': departments_with_classes,
            'departments_count': departments_count,
            'faculty_students_count': faculty_students_count,
            'faculties_teachers_count': faculties_teachers_count,
            'page_obj': page_obj,
            'faculty_id': faculty.pk,  # Add this line to pass faculty_id to the template
        })
        return context


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()

        subjects = department.subjects.filter(is_deleted=False)

        context.update({
            'subjects': subjects,
        })
        return context

class ClassDetailView(DetailView):
    model = Class
    template_name = 'academics/class_detail.html'
    context_object_name = 'class-detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_instance = self.get_object()

        subjects = class_instance.subjects.filter(is_deleted=False)
        subjects_paginator = Paginator(subjects, 3)  
        subjects_page_number = self.request.GET.get('subjects_page', 1)
        subjects_page_obj = subjects_paginator.get_page(subjects_page_number)

        students = Student.objects.filter(classroom=class_instance, is_deleted=False)
        students_paginator = Paginator(students, 2)  
        students_page_number = self.request.GET.get('students_page', 1)
        students_page_obj = students_paginator.get_page(students_page_number)

        department = class_instance.department
        students_count = students.count()
        teachers_count = Teacher.objects.filter(department=department, is_deleted=False).count()

        form = ClassSubjectForm(class_instance=class_instance)

        context.update({
            'department': department,
            'class_instance': class_instance,
            'students_count': students_count,
            'teachers_count': teachers_count,
            'subjects_page_obj': subjects_page_obj,
            'students_page_obj': students_page_obj,
            'form': form,
        })
        return context

    def post(self, request, *args, **kwargs):
        class_instance = self.get_object()
        form = ClassSubjectForm(request.POST, class_instance=class_instance)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            class_instance.subjects.add(subject)

            return redirect(reverse('class-detail', kwargs={'pk': class_instance.pk}))
        
        context = self.get_context_data(form=form)
        return self.render_to_response(context)







# Güncelleme View'ları
class FacultyUpdateView(UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'academics/faculty_form.html'
    success_url = reverse_lazy('manage')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Burada formun geçerli olduğunu kontrol edebilir veya ek işlemler yapabilirsiniz
        return response

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'academics/department_form_modal.html'
    success_url = reverse_lazy('department-list')

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
