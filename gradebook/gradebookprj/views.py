from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Access is denied")
        return wrapper
    return decorator

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':  # Проверка, является ли пользователь администратором
                return redirect('admin_dash')  # Перенаправление на страницу администратора
            elif user.role == 'teacher':  # Проверка, является ли пользователь учителем
                return redirect('teacher_dash')  # Перенаправление на страницу учителя
            elif user.role == 'student':  # Проверка, является ли пользователь студентом
                return redirect('student_dash')  # Перенаправление на страницу студента
            elif user.role == 'parent':  # Проверка, является ли пользователь родителем
                return redirect('parent_dash')  # Перенаправление на страницу родителя
            else:
                return redirect('home')  # Перенаправление на главную страницу для всех остальных ролей
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return redirect('login')  # Перенаправление на страницу авторизации в случае ошибки
    else:
        return render(request, 'login.html')

@role_required('admin')
def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        user_form = RegistrationForm(request.POST)
        if role == 'teacher':
            teacher_form = TeacherRegistrationForm(request.POST)
            if user_form.is_valid() and teacher_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()

                return redirect('admin_dash')
        elif role == 'parent':
            parent_form = ParentRegistrationForm(request.POST)
            if user_form.is_valid() and parent_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                parent = parent_form.save(commit=False)
                parent.user = user
                parent.save()

                return redirect('admin_dash')
        elif role == 'student':
            student_form = StudentRegistrationForm(request.POST)
            if user_form.is_valid() and student_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                student = student_form.save(commit=False)
                student.user = user
                student.save()

                return redirect('admin_dash')
    else:
        user_form = RegistrationForm()
        teacher_form = TeacherRegistrationForm()
        parent_form = ParentRegistrationForm()
        student_form = StudentRegistrationForm()
    
    return render(request, 'registration.html', {'user_form': user_form, 'teacher_form': teacher_form, 'parent_form': parent_form, 'student_form': student_form})

def logout_user(request):
    logout(request)
    return redirect('login') 

@role_required('admin')
def admin_dash(request):
    return render(request,'admin.html')

@role_required('admin')
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dash')  # Перенаправление на главную страницу администратора после создания предмета
    else:
        form = SubjectForm()
    return render(request, 'admin.html', {'form': form})

@role_required('admin')
def get_subjects(request):
    subjects = Subject.objects.all().values_list('subject_id', 'subject_name')
    subjects_list = [{'id': item[0], 'name': item[1]} for item in subjects]
    return JsonResponse({'subjects': subjects_list})

@role_required('admin')
def get_classes(request):
    classes = Classes.objects.all()
    classes_list = [{'id': cls.class_id, 'name': cls.class_name} for cls in classes]
    return JsonResponse({'classes': classes_list})

@role_required('admin')
def get_parents(request):
    parents = Parent.objects.all()
    parents_list = [{'id': parent.parent_id, 'name': parent.full_name} for parent in parents]
    return JsonResponse({'parents': parents_list})

@role_required('teacher')
def teacher_dash(request):
    return render(request,'teacher_dash.html')

@role_required('student')
def student_dash(request):
    return render(request,'student_dash.html')

@role_required('parent')
def parent_dash(request):
    return render(request,'parent_dash.html')

@role_required('admin')
def schedule_edit(request):
    weekdays = Weekday.objects.all()
    classes = Classes.objects.all()
    schedule_data = []
    for weekday in weekdays:
        schedule_items = Schedule.objects.filter(day_of_week=weekday)
        schedule_data.append((weekday, schedule_items))
    context = {
        'schedule_data': schedule_data,
        'classes': classes,
        'weekdays': weekdays,
    }
    return render(request, 'schedule_edit.html', context)

def rate_view(request, subject_id, class_id):
    subject = Subject.objects.get(pk=subject_id)
    students = Student.objects.filter(class_id=class_id)
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            date = form.cleaned_data['date']
            student_id = form.cleaned_data['student_id'].pk  # Используйте .id для получения первичного ключа
            student = Student.objects.get(pk=student_id)
            new_grade = Grade(
                grade=grade,
                date=date,
                subject_id=subject,
                student_id=student
            )
            new_grade.save() 
            return redirect('schedule')
    else:
        form = GradeForm(initial={'class_id': class_id})
    
    context = {
        'subject': subject,
        'students': students,
        'form': form,
    }
    return render(request, 'rate.html', context)
