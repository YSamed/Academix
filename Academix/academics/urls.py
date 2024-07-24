from django.urls import path
from .views import (FacultyListView, DepartmentListView, ClassListView,FacultyDetailView, DepartmentDetailView, ClassDetailView,FacultyUpdateView, DepartmentUpdateView, ClassUpdateView,FacultyDeleteView, DepartmentDeleteView, ClassDeleteView,manage_academics)

urlpatterns = [
    path('manage-academics/', manage_academics, name='manage-academics'),

    # Listeleme
    path('faculties/', FacultyListView.as_view(), name='faculty-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('classes/', ClassListView.as_view(), name='class-list'),

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
