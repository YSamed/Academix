from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    subjects = models.ManyToManyField('Subject', related_name='classes', blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.department.name} {self.name}" if self.department else self.name
class Subject(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    code = models.CharField(max_length=10, unique=True)
    total_classes = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
