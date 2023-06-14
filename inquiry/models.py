from django.db import models
from hrm.models import *
# Create your models here.
class Purpose(models.Model):
    purpose = models.CharField(max_length=255)
    def __str__(self):
        return self.purpose
    
    class Meta:
        verbose_name_plural = "01. Inquiry Purpose"

class InquiryStage(models.Model):
    stage = models.CharField(max_length=200)
    def __str__(self):
        return self.stage

    class Meta:
        verbose_name_plural = "02.  Stage"

class Inquiry(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    purpose = models.CharField(max_length=255)
    stage = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    education_qualification = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    closed_reason = models.TextField(null=True, blank=True)

    consultation_date = models.DateTimeField(blank=True, null=True)
    assigned = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    
    class Meta:
        verbose_name_plural = "03. Inquiries"



class InquiryLogs(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    changed_by = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.changed_by} - {self.activity}"
    
    class Meta:
        verbose_name_plural = "04. Inquiry Logs"

class InquiryNotes(models.Model):
    inquiry = models.ForeignKey(Inquiry,on_delete=models.CASCADE)
    note_title = models.CharField(max_length = 255)
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inquiry.first_name

    class Meta:
        verbose_name_plural = "05. Inquiry Notes"
