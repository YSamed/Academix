from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'is_deleted')
    search_fields = ('user__username', 'user__email', 'classroom__name')
