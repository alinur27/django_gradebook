from django.contrib import admin
from .models import *

admin.site.register([Class, Parent, Teacher, Student, Schedule, Grade, Subject])
