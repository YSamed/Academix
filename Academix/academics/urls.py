from django.urls import path
from .views import (
faculty_form,delete_faculty,FacultyListView,FacultyDetailView,
department_form,delete_department,DepartmentListView,DepartmentDetailView,
class_form, delete_class,ClassListView,ClassDetailView,
AddSubjectView,get_subjects,
index,ManageView
)

urlpatterns = [
    # Ana sayfa ve yönetim
    path('', index, name='index'),
    path('manage/', ManageView.as_view(), name='manage'),


    # Fakülte 
    path('faculty/add/', faculty_form, name='faculty-create'),
    path('faculty/<int:pk>/edit/', faculty_form, name='faculty-update'),
    path('faculty/<int:pk>/delete/', delete_faculty ,name='faculty-delete'),
    path('faculty/list/', FacultyListView.as_view(), name='faculty-list'),
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),


    # Bölüm
    path('department/add/', department_form, name='department-create'),
    path('department/<int:pk>/edit/', department_form, name='department-update'),
    path('department/delete/<int:pk>/', delete_department, name='department-delete'),
    path('department/add/<int:faculty_id>/', department_form, name='department-create-with-faculty'),
    path('department/list/', DepartmentListView.as_view(), name='department-list'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),


    # Sınıf 
    path('class/add/', class_form, name='class-create'),
    path('class/<int:pk>/edit/', class_form, name='class-update'),
    path('class/delete/<int:pk>/', delete_class, name='class-delete'),
    path('class/list/', ClassListView.as_view(), name='class-list'),
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),


    # Ders
    path('add-subject/', AddSubjectView.as_view(), name='add-subject'),
    path('get_subjects/', get_subjects, name='get_subjects'),

]
