from django.urls import path
from .views import (index, manage,faculty_form, department_form, class_form,get_subjects, delete_department,AddSubjectView,FacultyListView, DepartmentListView, ClassListView,FacultyDetailView, DepartmentDetailView, ClassDetailView,FacultyUpdateView, DepartmentUpdateView, ClassUpdateView,FacultyDeleteView, DepartmentDeleteView, ClassDeleteView)


urlpatterns = [

    path('', index, name='index'),
    path('manage', manage, name='manage'),

    path('department_form/<int:faculty_id>/', department_form, name='department_form'),
    path('class_form/<int:faculty_id>/', class_form, name='class_form'),
    path('faculty_form/', faculty_form, name='faculty_form'),
    path('department_form/', department_form, name='department_form'),
    path('class_form/', class_form , name='class_form'),
    path('add-subject/', AddSubjectView.as_view(), name='add_subject'),
    path('get_subjects/', get_subjects, name='get_subjects'),

    # Listeleme
    path('faculty_list/', FacultyListView.as_view(), name='faculty_list'),
    path('department_list/', DepartmentListView.as_view(), name='department_list'),
    path('class_list/', ClassListView.as_view(), name='class_list'),
    
    # Detay
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),







    # Güncelleme
    path('faculty/<int:pk>/edit/', FacultyUpdateView.as_view(), name='faculty-update'),

    path('department/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department-update'),

    
    path('class/<int:pk>/edit/', ClassUpdateView.as_view(), name='class-update'),







    # Silme
    path('department/delete/<int:pk>/', delete_department, name='department-delete'),
    path('faculty/<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty-delete'),
    path('class/<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
 ]

