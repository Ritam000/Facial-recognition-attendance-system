from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'enrollment_number','name', 'phone', 'gender', 'stream', 'photo']