from django import forms
from .models import Faculty, Department, Class, Subject
from django.forms import formset_factory


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'faculty']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'department', 'subjects']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'department', 'code', 'total_classes']



FacultyFormSet = formset_factory(FacultyForm, extra=1)
DepartmentFormSet = formset_factory(DepartmentForm, extra=1)
ClassFormSet = formset_factory(ClassForm, extra=1)