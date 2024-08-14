from django import forms
from .models import Subject

class AttendanceForm(forms.Form):
    subject_ids = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),  # Başlangıçta boş
        widget=forms.CheckboxSelectMultiple,  # Çekmece seçimi
        required=True,
    )

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            self.fields['subject_ids'].queryset = teacher.subjects.all()
