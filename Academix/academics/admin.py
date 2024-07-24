from django.contrib import admin
from academics.models import Faculty , Department , Class , Subject
# Register your models here.

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Subject)