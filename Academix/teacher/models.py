from django.db import models
from django.contrib.auth.models import User
from academics.models import Department, Subject

# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.employee_id})'
