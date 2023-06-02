from django.db import models
from student.models import*
from course.models import*

# Create your models here.
class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null = True)
    misc_name = models.CharField(max_length=255,null = True, blank = True)
    misc_amount = models.FloatField(null = True, blank = True)
    discount = models.FloatField(null = True, blank = True)
    vat_amount = models.FloatField(null = True, blank = True)
    remarks = models.CharField(max_length = 255, null = True, blank = True)
    created_by = models.CharField(max_length = 255, null = True, blank = True)
    due_date = models.DateField()
    invoice_amount = models.FloatField(null = True, blank = True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Invoice"

    class Meta:
        verbose_name_plural="0.1 Invoices"
   


