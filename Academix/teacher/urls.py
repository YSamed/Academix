from django.urls import path
from .views import TeacherListViews, TeacherDetailViews, TeacherCreateViews, TeacehrUpdateViews , TeacherDeleteView

urlpatterns = [
    path('', TeacherListViews.as_view(), name='teacher-list'),
    path('<int:pk>/', TeacherDetailViews.as_view(), name='teacher-detail'),
    path('create/', TeacherCreateViews.as_view(), name='teacher-create'),
    path('<int:pk>/update/', TeacehrUpdateViews.as_view(), name='teacher-update'),
    path('<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher-delete'),
]
