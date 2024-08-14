from django.urls import path
from .views import TeacherListViews, TeacherDetailViews, TeacherCreateViews, TeacehrUpdateViews , TeacherLoginView ,TeacherLogoutView , delete_teacher 

app_name = 'teachers'

urlpatterns = [
    path('', TeacherListViews.as_view(), name='teacher-list'),
    path('<int:pk>/', TeacherDetailViews.as_view(), name='teacher-detail'),
    path('create/', TeacherCreateViews.as_view(), name='teacher-create'),
    path('<int:pk>/update/', TeacehrUpdateViews.as_view(), name='teacher-update'),
    path('teacher/<int:pk>/delete/', delete_teacher, name='teacher-delete'),


    path('login/', TeacherLoginView.as_view(), name='login'),
    path('logout/', TeacherLogoutView.as_view(), name='logout'),
]
