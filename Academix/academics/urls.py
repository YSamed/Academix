from django.urls import path
from .views import (
    index, manage, faculty_form,  class_form, get_subjects,
    delete_department, AddSubjectView, DepartmentCreateView,
    FacultyListView, DepartmentListView, ClassListView,
    FacultyDetailView, DepartmentDetailView, ClassDetailView,
    FacultyUpdateView, DepartmentUpdateView, ClassUpdateView,
    FacultyDeleteView, DepartmentDeleteView, ClassDeleteView
)

urlpatterns = [
    # Ana sayfa ve yönetim
    path('', index, name='index'),
    path('manage/', manage, name='manage'),
    path('department/delete/<int:pk>/', delete_department, name='department-delete'),


    # Fakülte formu (ekleme ve güncelleme)
    path('faculty/add/', faculty_form, name='faculty-create'),
    path('faculty/<int:pk>/edit/', faculty_form, name='faculty-update'),



    # Bölüm formu (ekleme ve güncelleme)
    path('department/add/', DepartmentCreateView.as_view(), name='department-create'),
    path('department/add/<int:faculty_id>/', DepartmentCreateView.as_view(), name='department-create-with-faculty'),



    # Sınıf formu (ekleme ve güncelleme)
    path('class/add/', class_form, name='class-create'),
    path('class/<int:pk>/edit/', class_form, name='class-update'),

    # Konu ekleme
    path('add-subject/', AddSubjectView.as_view(), name='add-subject'),

    # Konu alma
    path('get_subjects/', get_subjects, name='get_subjects'),

    # Listeleme
    path('faculty/list/', FacultyListView.as_view(), name='faculty-list'),
    path('department/list/', DepartmentListView.as_view(), name='department-list'),
    path('class/list/', ClassListView.as_view(), name='class-list'),

    # Detay
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),

    # Silme
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),
    path('faculty/<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty-delete'),
    path('class/<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
]
