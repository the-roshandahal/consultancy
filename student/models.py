from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.first_name
    class Meta:
        verbose_name_plural = "01. Students"

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file_name=models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f" {self.student.user.first_name}: {self.file_name}"