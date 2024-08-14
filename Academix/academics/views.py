from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView,CreateView ,View
from django.urls import reverse, reverse_lazy
from django.http import  JsonResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Faculty, Department, Class, Subject
from students.models import Student
from teacher.models import Teacher
from .forms import FacultyForm, DepartmentForm, ClassForm, SubjectForm ,ClassSubjectForm
from django.http import HttpResponseForbidden


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
        'breadcrumb': [
            {'url': reverse('index'), 'name': 'Anasayfa'}
        ]
    }
    return render(request, 'academics/index.html', context)


class ManageView(View):

    def dispatch(self, request, *args, **kwargs):      
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.groups.filter(name='Yönetici').exists() or 
                request.user.groups.filter(name='Öğretmen').exists()):
            return HttpResponseForbidden("Bu Sayfaya Erişim İzniniz Yok")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        faculty_form = FacultyForm()
        context = {
            'faculty_form': faculty_form,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'name': 'Yönetici Paneli', 'active': True}
            ]
        }
        return render(request, 'academics/manager.html', context)

    def post(self, request, *args, **kwargs):
        faculty_form = FacultyForm(request.POST)
        if faculty_form.is_valid():
            faculty_form.save()
            return redirect('manage')
        
        context = {
            'faculty_form': faculty_form,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'name': 'Yönetici Paneli', 'active': True}
            ]
        }
        return render(request, 'academics/manager.html', context)



# Fakülte 
def faculty_form(request, pk=None):
    if pk:
        faculty = get_object_or_404(Faculty, pk=pk)
        if request.method == 'POST':
            form = FacultyForm(request.POST, instance=faculty)
            if form.is_valid():
                form.save()
                messages.success(request, 'Fakülte başarıyla güncellendi.')
                return redirect('manage')
            else:
                messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
        else:
            form = FacultyForm(instance=faculty)
        breadcrumb = [
            {'url': reverse('index'), 'name': 'Anasayfa'},
            {'url': reverse('faculty-list'), 'name': 'Fakülteler'},
            {'url': reverse('faculty-form', args=[pk]), 'name': 'Fakülte Ekle'}
        ]
    else:
        if request.method == 'POST':
            form = FacultyForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Fakülte başarıyla oluşturuldu.')
                return redirect('faculty-list')
            else:
                messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
        else:
            form = FacultyForm()
        breadcrumb = [
            {'url': reverse('index'), 'name': 'Anasayfa'},
            {'url': reverse('faculty-list'), 'name': 'Fakülteler'},
            {'name': ' Fakülte Ekle', 'active': True}
        ]
    
    context = {
        'form': form,
        'breadcrumb': breadcrumb
    }
    return render(request, 'academics/faculty_form.html', context)

def delete_faculty(request , pk ):
    faculty = get_object_or_404(Faculty,pk=pk)
    faculty.is_deleted = True
    faculty.save()
    messages.success(request, f"{faculty.name} başarıyla silindi.")
    return redirect(reverse('faculty-list'))

class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculties/faculty_list.html'
    context_object_name = 'faculties'
    paginate_by= 8

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
        
        paginator = Paginator(faculties, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'total_faculties': total_faculties,
            'total_departments': total_departments,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'faculties': faculties,
            'page_obj' :page_obj,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'url': reverse('manage'), 'name': 'Yönetici Paneli'},
                {'url': reverse('faculty-list'), 'name': 'Fakülteler'},
            ]
        })
        return context
  
class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'academics/faculty_detail.html'
    context_object_name = 'faculty'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.get_object()
        
        departments = faculty.departments.filter(is_deleted=False)
        departments_count = departments.count()
        faculty_students_count = Student.objects.filter(classroom__department__in=departments, is_deleted=False).count()
        faculties_teachers_count = Teacher.objects.filter(department__in=departments, is_deleted=False).count()
        
        paginator = Paginator(departments, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
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
            'faculty_id': faculty.pk,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'url': reverse('faculty-list'), 'name': 'Fakülteler'},
                {'url': reverse('faculty-detail', args=[faculty.pk]), 'name': faculty.name}
            ]
        })
        return context


# Bölüm
def department_form(request, pk=None, faculty_id=None):
    if pk:
        # Düzenleme işlemi için mevcut department nesnesini al
        department = get_object_or_404(Department, pk=pk)
        if request.method == 'POST':
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                updated_department = form.save(commit=False)
                if faculty_id:
                    faculty = get_object_or_404(Faculty, id=faculty_id)
                    updated_department.faculty = faculty
                updated_department.save()
                messages.success(request, 'Bölüm başarıyla güncellendi.')
                return redirect('manage')
            else:
                messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
        else:
            form = DepartmentForm(instance=department, faculty_id=faculty_id)
    else:
        # Yeni department ekleme işlemi
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                new_department = form.save(commit=False)
                if faculty_id:
                    faculty = get_object_or_404(Faculty, id=faculty_id)
                    new_department.faculty = faculty
                new_department.save()
                messages.success(request, 'Bölüm başarıyla oluşturuldu.')
                return redirect('manage')
            else:
                messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
        else:
            form = DepartmentForm(faculty_id=faculty_id)

    # Breadcrumb oluşturma
    breadcrumb = [
        {'url': reverse('index'), 'name': 'Anasayfa'},
        {'url': reverse('department-list'), 'name': 'Bölümler'}
    ] 
    if pk:
        breadcrumb.append({'url': reverse('faculty-detail', args=[pk]), 'name': department.name})
        breadcrumb.append({'url': '#', 'name': 'Bölümü Güncelle'})
    else:
        if faculty_id:
            faculty = get_object_or_404(Faculty, id=faculty_id)
            breadcrumb.append({'url': reverse('faculty-detail', args=[faculty.id]), 'name': faculty.name})
        breadcrumb.append({'url': '#', 'name': 'Yeni Bölüm'})
    
    context = {
        'department_form': form,
        'breadcrumb': breadcrumb
    }
    
    return render(request, 'academics/department_form.html', context)

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.is_deleted = True
    department.save()
    messages.success(request, f"{department.name} başarıyla silindi.")
    return redirect(reverse('faculty-detail', kwargs={'pk': department.faculty.pk}))

class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'
    paginate_by = 8

    def get_queryset(self):
        queryset = Department.objects.filter(is_deleted=False).annotate(
            teacher_count=Count('teachers', filter=Q(teachers__is_deleted=False)),
            subject_count=Count('subjects', filter=Q(subjects__is_deleted=False))
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_departments = Department.objects.filter(is_deleted=False).count()
        total_teachers = Teacher.objects.filter(is_deleted=False).count()
        total_students = Student.objects.filter(is_deleted=False).count()
        total_subjects = Subject.objects.filter(is_deleted=False).count()

        for department in context['departments']:
            department.student_count = Student.objects.filter(
                classroom__department=department, is_deleted=False
            ).count()

            if total_teachers > 0:
                department.teacher_percentage = (department.teacher_count / total_teachers) * 100
            else:
                department.teacher_percentage = 0

            if total_students > 0:
                department.student_percentage = (department.student_count / total_students) * 100
            else:
                department.student_percentage = 0

            if total_subjects > 0:
                department.subject_percentage = (department.subject_count / total_subjects) * 100
            else:
                department.subject_percentage = 0

        context.update({
            'total_departments': total_departments,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'total_subjects': total_subjects,
            'breadcrumb': [
                {'url': reverse('index'), 'name': 'Anasayfa'},
                {'url': reverse('manage'), 'name': 'Yönetici Paneli'},
                {'url': reverse('department-list'), 'name': 'Bölümler'},
            ]
        })

        return context

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'

    def get(self, request, *args, **kwargs):
        department = self.get_object()
        faculty = department.faculty_set.first()
        if faculty:
            return redirect(reverse('faculty-detail', args=[faculty.id]))
        else:
            return redirect('department-list')



#Sınıf
def class_form(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sınıf başarıyla oluşturuldu.')
            return redirect('manage')
        else:
            messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
    else:
        form = ClassForm()

    breadcrumb = [
        {'url': reverse('index'), 'name': 'Anasayfa'},
        {'url': reverse('manage'), 'name': 'Yönetici Paneli '},
        {'url': '#', 'name': 'Sınıf Ekle'}
    ]

    return render(request, 'academics/class_form.html', {
        'class_form': form,
        'breadcrumb': breadcrumb
    })

def delete_class(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    class_obj.is_deleted = True
    class_obj.save()
    messages.success(request, f"{class_obj.name} başarıyla silindi.")
    
    # Fakülteye yönlendirme
    return redirect(reverse('class-list'))

class ClassListView(ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'  
    paginate_by = 8


    def get_queryset(self):
        return Class.objects.filter(is_deleted=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_classes'] = Class.objects.filter(is_deleted=False).count()
       
        context['breadcrumb'] = [
            {'url': reverse('index'), 'name': 'Anasayfa'},
            {'url': reverse('manage'), 'name': 'Yönetici Paneli'},
            {'url': reverse('class-list'), 'name': 'Sınıflar'}
        ]
        
        return context

class ClassDetailView(DetailView):
    model = Class
    template_name = 'academics/class_detail.html'
    context_object_name = 'class_instance'

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
        faculty = department.faculty 

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
            'faculty': faculty,  
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




# Ders 
class AddSubjectView(CreateView):
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Yetkilendirme kontrolü
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.groups.filter(name='Yönetici').exists() or 
                request.user.groups.filter(name='Öğretmen').exists()):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['class_id'] = self.kwargs.get('class_id', None)  
        return kwargs

    def form_valid(self, form):
        SubjectForm = form.save()
        
        class_id = self.kwargs.get('class_id', None)
        
        if class_id:
            return redirect('class_detail', pk=class_id)
        return redirect('manage')


def get_subjects(request):
    department_id = request.GET.get('department_id')
    if department_id:
        subjects = Subject.objects.filter(department_id=department_id)
        subjects_list = list(subjects.values('id', 'name'))
    else:
        subjects_list = []

    return JsonResponse({'subjects': subjects_list})






