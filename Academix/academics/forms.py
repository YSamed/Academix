from django import forms
from .models import Faculty, Department, Class, Subject
from django.forms import formset_factory


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),}

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department 
        fields = ['faculty' , 'name']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['department', 'name', 'subjects']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'subjects': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
    


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['department','name', 'code', 'total_classes']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'total_classes': forms.TextInput(attrs={'class': 'form-control' }),

            
        }


