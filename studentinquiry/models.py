from django.db import models
from hrm.models import *
# Create your models here.


class InquiryStage(models.Model):
    stage = models.CharField(max_length=200)
    def __str__(self):
        return self.stage

    class Meta:
        verbose_name_plural = "02.  Stage"


class InquiryPurpose(models.Model):
    stage = models.CharField(max_length=200)
    def __str__(self):
        return self.stage

    class Meta:
        verbose_name_plural = "02.  Stage"

class StudentInquiry(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob=models.DateField(auto_now=True)
    guardian_name = models.CharField(max_length=255)
    marital_status=models.CharField(max_length=255,default="Single")
    email = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    temporary_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    purpose = models.ForeignKey(InquiryPurpose,on_delete=models.CASCADE,null=True,blank=True)
    
    
    institution1 = models.CharField(max_length=100,null=True,blank=True)
    passed_year1 = models.PositiveIntegerField(null=True,blank=True)
    percentage1 = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)

    institution2 = models.CharField(max_length=100,null=True,blank=True)
    passed_year2 = models.PositiveIntegerField(null=True,blank=True)
    percentage2 = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)

    institution3 = models.CharField(max_length=100,null=True,blank=True)
    passed_year3 = models.PositiveIntegerField(null=True,blank=True)
    percentage3 = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
 
    
    course = models.CharField(max_length=100,default=True)
    college = models.CharField(max_length=100,default=True)
    country = models.CharField(max_length=100,default=True)
    city = models.CharField(max_length=100,default=True)
    intake = models.CharField(max_length=100,default=True)
    applied_country = models.CharField(max_length=100, blank=True, null=True)
    applied_date = models.DateField(blank=True, null=True)
    other=models.CharField(max_length=255,blank=True, null=True)
    
    date = models.DateTimeField(blank=True, null=True)
    remarks= models.CharField(max_length=255,null=True,blank=True)
    assigned = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    
    class Meta:
        verbose_name_plural = "03. Inquiries"                                          



class InquiryLogs(models.Model):
    inquiry = models.ForeignKey(StudentInquiry, on_delete=models.CASCADE)
    changed_by = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.changed_by} - {self.activity}"
    
    class Meta:
        verbose_name_plural = "04. Inquiry Logs"


class InquiryNote(models.Model):
    inquiry = models.ForeignKey(StudentInquiry,on_delete=models.CASCADE)
    note_title = models.CharField(max_length = 255)
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inquiry.first_name

    class Meta:
        verbose_name_plural = "05. Inquiry Note"