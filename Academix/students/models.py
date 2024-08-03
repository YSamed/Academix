from django.db import models
from django.contrib.auth.models import User
from academics.models import Class, Subject

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    additional_subjects = models.ManyToManyField(Subject, related_name='additional_students', blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})'
