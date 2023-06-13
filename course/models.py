from django.db import models

# Create your models here.



class CourseCategory(models.Model):
    course_category = models.CharField(max_length=255)
    def __str__(self):
        return self.course_category
    class Meta:
        verbose_name_plural = "01. Courses Category"


class Course(models.Model):
  
    course_title = models.CharField(max_length=255)
    course_price = models.FloatField()
    course_description = models.TextField(null = True, blank = True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, blank=True, null=True,)
    
    def __str__(self):
        return self.course_title
    class Meta:
        verbose_name_plural = "02. Courses"      

class Service(models.Model):
  
    service_title = models.CharField(max_length=255)
    service_price = models.FloatField()
    service_description = models.TextField(null = True, blank = True)
    service_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, blank=True, null=True,)
    
    def __str__(self):
        return self.service_title
    class Meta:
        verbose_name_plural = "03. services"      


