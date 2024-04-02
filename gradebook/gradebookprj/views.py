from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'index.html')

def teacher_dashboard(request):
    # Получаем информацию об учителе (здесь предполагается, что у вас есть модель Teacher)
    teacher = Teacher.objects.get(user=request)  # Предположим, что у каждого учителя есть поле user для связи с пользователем Django
    # Получаем список классов учителя
    classes = Class.objects.filter(teacher=teacher)
    # Получаем список студентов в этих классах
    students = Student.objects.filter(class_id__in=classes)
    # Получаем список оценок этих студентов
    grades = Grade.objects.filter(student_id__in=students)

    context = {
        'teacher': teacher,
        'classes': classes,
        'students': students,
        'grades': grades,
    }
    return render(request, 'teacher_dashboard.html', context)