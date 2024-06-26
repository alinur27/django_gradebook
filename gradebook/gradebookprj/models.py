from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)

    def __str__(self):
        return self.class_name

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher', null=True)
    teacher_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.full_name

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent', null=True)
    parent_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.full_name

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student', null=True)
    student_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    birth_date = models.DateField()
    phone_number = models.IntegerField()
    email = models.EmailField()
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

class Grade(models.Model):
    grade = models.IntegerField()
    date = models.DateField()
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.student_id.full_name} - {self.subject_id.subject_name} - Grade: {self.grade} - Date: {self.date}"
    
class Weekday(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey('Subject', on_delete=models.CASCADE)
    class_id = models.ForeignKey('Classes', on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    day_of_week = models.ForeignKey(Weekday, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_id} - {self.class_id} - {self.teacher_id} - {self.day_of_week}"
