from django import forms
from teacher.models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'employee_id', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teacher ID'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
