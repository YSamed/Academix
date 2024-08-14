from django import forms
from django.contrib.auth.models import User
from students.models import Student

class StudentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        required=True
    )
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'classroom']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        password2 = clean_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('Şifreler Eşleşmiyor')


    def save(self, commit=True):
        # Kullanıcıyı oluşturma
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        student = super().save(commit=False)
        # Kullanıcıyı öğrenciye atama işlemi
        student.user = user
        if commit:
            student.save()
        return student
