from django.db import models
from django.contrib.auth.models import User
from course.models import *
from hrm.models import *
# Create your models here.
from course.models import *


class EnrollmentType(models.Model):
    enrollment_type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.enrollment_type
    class Meta:
        verbose_name_plural = "01. Enrollment Type"

class StudentStage(models.Model):
    stage = models.CharField(max_length=200)
    def __str__(self):
        return self.stage

    class Meta:
        verbose_name_plural = "02.  Stage"

class StudentSource(models.Model):
    source = models.CharField(max_length=200)
    def __str__(self):
        return self.source

    class Meta:
        verbose_name_plural = "03.  Sources"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    enrollment_type = models.ForeignKey(EnrollmentType, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(StudentSource, on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.ForeignKey(StudentStage, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ManyToManyField(Employee)
    course = models.ManyToManyField(Course)
    log_status = models.BooleanField(default=True)
    active = models.BooleanField(default=1)
    date_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name
    class Meta:
        verbose_name_plural = "02. Student"



class StudentLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    changed_by = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.user.first_name

    class Meta:
        verbose_name_plural = "04. Activity Log"


class StudentCall(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    called_by = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    summary = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student.user.first_name

    class Meta:
        verbose_name_plural = "05. Student Call"



class StudentNotes(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    note_title = models.CharField(max_length = 255)
    note = models.TextField()
    def __str__(self):
        return self.student.user.first_name

    class Meta:
        verbose_name_plural = "06. Student Notes"


class StudentFiles(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='Student_file/')
    added_by = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.user.first_name

    class Meta:
        verbose_name_plural = "06. Student Files"

