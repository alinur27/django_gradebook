from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('admin_dash/', admin_dash, name='admin_dash'),
    path('teacher_dash/', teacher_dash, name='teacher_dash'),
    path('student_dash/', student_dash, name='student_dash'),
    path('parent_dash/', parent_dash, name='parent_dash'),
    path('logout/', logout_user, name='logout'),
    path('create_subject/', create_subject, name='create_subject'),
    path('get_subjects/', get_subjects, name='get_subjects'),
    path('get_classes/', get_classes, name='get_classes'),
    path('get_parents/', get_parents, name='get_parents'),
    path('schedule/', schedule_edit, name='schedule'),
    path('rate/<int:subject_id>/<int:class_id>/', rate_view, name='rate'),
]