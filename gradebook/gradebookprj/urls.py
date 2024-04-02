from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
]