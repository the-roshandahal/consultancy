from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render
from decimal import Decimal
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from account.models import *
from course.models import *
from student.models import *
from .models import *
from account.context_processors import custom_data_views
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Q
from datetime import datetime,date,timedelta

# Create your views here.
def invoice(request):
    if 'read_finance' in custom_data_views(request):
        invoices = Invoice.objects.all()
        context={
            'invoices':invoices
            }
        return render (request, 'finance/invoices.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_invoice(request):
    if 'create_finance' in custom_data_views(request):
        if request.method == "POST":
            student = request.POST["student"]
            selected_course_ids = request.POST.getlist("selected_course")
            selected_course_amounts = request.POST.getlist("selected_course_amount")
            selected_course_discounts = request.POST.getlist("selected_course_discount")
            selected_course_quantities = request.POST.getlist("selected_course_quantity")
            misc_name = request.POST["misc_name"]
            misc_amount = Decimal(request.POST["misc_amount"])
            due_date = request.POST["due_date"]
            remarks = request.POST["remarks"]
            student=Student.objects.get(id=student)
            # create the invoice instance
            invoice = Invoice.objects.create(
                student=student,
                misc_name=misc_name,
                misc_amount=misc_amount,
                due_date=due_date,
                remarks=remarks,
                created_by=request.user.username,
            )
            
            # calculate the invoice amount
            invoice_amount = misc_amount
            for i in range(len(selected_course_ids)):
                course_id = selected_course_ids[i]
                course_amount = Decimal(selected_course_amounts[i])
                course_discount = Decimal(selected_course_discounts[i])
               
                course_total = (course_amount - course_discount) 
                invoice_amount += course_total
            invoice.invoice_amount = invoice_amount
            
            # # calculate the VAT amount
            # if selected_course_ids and Course.objects.filter(id__in=selected_course_ids, is_vatable=True).exists():
            #     vat_rate = Decimal("0.12") # assume VAT rate is 12%
            #     vat_amount = invoice_amount * vat_rate
            #     invoice.vat_amount = vat_amount
            
            # save the invoice instance
            invoice.save()
            
            # create the invoice course instances
            for i in range(len(selected_course_ids)):
                course_id = selected_course_ids[i]
                course_amount = Decimal(selected_course_amounts[i])
                course_discount = Decimal(selected_course_discounts[i])
               
                course = Course.objects.get(id=course_id)
                InvoiceCourse.objects.create(
                    invoice=invoice,
                    course=course,
                  
                    course_price=course_amount - course_discount,
                )
               
                course.save()
            details = invoice.id
            details = "INV_NO_"+str(details)
            if(Statement.objects.filter(student=student).exists()):

                bal = Statement.objects.filter(
                    student=student).order_by('-id')[:1].get()
                initial_balance = bal.balance
                balance = float(initial_balance) + float(invoice_amount)

                Statement.objects.create(
                    student=student, transaction='invoice', details=details, amount=invoice_amount, balance=balance)
            else:
                amount = 0
                payment = 0
                balance = 0
                Statement.objects.create(student=student, transaction='Opening Balance',
                                        details='--', amount=amount, payment=payment, balance=balance)

                bal = Statement.objects.filter(
                    student=student).order_by('-id')[:1].get()
                initial_balance = bal.balance
                balance = float(initial_balance) + float(invoice_amount)

                Statement.objects.create(
                    student=student, transaction='invoice', details=details, amount=invoice_amount, balance=balance)
            messages.info(request, "Invoice Created Successfully.")
            return redirect(view_invoice, id=invoice.id)
        else:
            course = Course.objects.all()
            student = Student.objects.all()
            context = {
                'course': course,
                'student': student
            }
            return render(request, "finance/create_invoice.html", context)


def view_invoice(request, id):
    if 'read_finance' in custom_data_views(request):
        invoice = Invoice.objects.get(id=id)
        course = InvoiceCourse.objects.filter(invoice_id=id)
        context = {
            'course':course,
            'invoice': invoice,
        }
        return render(request, 'finance/view_invoice.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


