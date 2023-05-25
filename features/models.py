from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_email = models.CharField(max_length=255)
    company_contact_number = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_images/')
    payment_terms = models.TextField()
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "03. Company Setup"