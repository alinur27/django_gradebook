from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']

class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ['class_name']

class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'subject', 'phone_number', 'email']

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'class_id', 'birth_date', 'phone_number', 'email', 'parent_id']

class ParentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['full_name', 'phone_number', 'email']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade', 'date', 'student_id']

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        super(GradeForm, self).__init__(*args, **kwargs)
        if class_id:
            self.fields['student_id'].queryset = Student.objects.filter(class_id=class_id)