from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'is_deleted')
    search_fields = ('user__username', 'user__email', 'department__name')
