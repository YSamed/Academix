from django import forms
from .models import Faculty, Department, Class, Subject


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

    def __init__(self, *args, **kwargs):
        faculty_id = kwargs.pop('faculty_id', None)
        super().__init__(*args, **kwargs)
        if faculty_id:
            self.fields['faculty'].initial = faculty_id

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

    def __init__(self, *args, **kwargs):
            class_id = kwargs.pop('class_id', None)
            super().__init__(*args, **kwargs)
            self.class_id = class_id

class ClassSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        class_instance = kwargs.pop('class_instance', None)
        super().__init__(*args, **kwargs)

        if class_instance:
            department = class_instance.department
            self.fields['subject'].queryset = Subject.objects.filter(department=department, is_deleted=False)
        else:
            self.fields['subject'].queryset = Subject.objects.none()
