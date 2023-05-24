from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField('Student', related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

    
    
    def __str__(self):
	    return self.title
	    


	
class Student(models.Model):
    student_id = models.CharField(max_length=100, primary_key=True)
    name=models.CharField(default='admin',max_length=100)
    last_name=models.CharField(default='admin',max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=20)
    course = models.ManyToManyField(Course, through='Enrollment', related_name='enrolled_students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.name
    


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    

    class Meta:
        unique_together = ['student', 'course']

        def __str__(self):
             return self.name
	    
class Document(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.course} - {self.student}: {self.file.name}"

