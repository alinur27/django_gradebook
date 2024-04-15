from django.contrib import admin
from .models import *

admin.site.register([CustomUser, Classes, Subject, Teacher, Parent, Student, Grade, Schedule, Weekday])
