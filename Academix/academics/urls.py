from django.urls import path
from .views import (index, manage,faculty_form, department_form, class_form, subjects_form ,get_subjects,FacultyListView, DepartmentListView, ClassListView,FacultyDetailView, DepartmentDetailView, ClassDetailView,FacultyUpdateView, DepartmentUpdateView, ClassUpdateView,FacultyDeleteView, DepartmentDeleteView, ClassDeleteView,)


urlpatterns = [

    path('', index, name='index'),
    path('manage', manage, name='manage'),
    path('faculty_form/', faculty_form, name='faculty_form'),
    path('department_form/', department_form, name='department_form'),
    path('class_form/', class_form , name='class_form'),
    path ('subjects_form/', subjects_form, name=('subjects_form')),
    path('get_subjects/', get_subjects, name='get_subjects'),




    # Listeleme
    path('faculty_list/', FacultyListView.as_view(), name='faculty_list'),
    path('department_list/', DepartmentListView.as_view(), name='department_list'),
    path('class_list/', ClassListView.as_view(), name='class_list'),


    # Detay
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),

    # Güncelleme
    path('faculty/<int:pk>/edit/', FacultyUpdateView.as_view(), name='faculty-update'),
    path('department/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department-update'),
    path('class/<int:pk>/edit/', ClassUpdateView.as_view(), name='class-update'),

    # Silme
    path('faculty/<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty-delete'),
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),
    path('class/<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
 ]

