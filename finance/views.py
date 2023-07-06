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

                InvoiceCourse.objects.create(
                    invoice=invoice,
                    course=course_id,
                    course_price=course_amount - course_discount,
                )
               
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
            service = Service.objects.all()
            student = Student.objects.all()
            tomorrow = datetime.now().date() + timedelta(days=2)
            default_due_date = tomorrow.strftime("%Y-%m-%d")

            context = {
                'course': course,
                'student': student,
                'service':service,
                'due_date':default_due_date,

            }
            return render(request, "finance/create_invoice.html", context)


def view_invoice(request, id):
    if 'read_finance' in custom_data_views(request):
        invoice = Invoice.objects.get(id=id)
        course = InvoiceCourse.objects.filter(invoice_id=id)
        print('hello')
        print(course)
        context = {
            'course':course,
            'invoice': invoice,
        }
        return render(request, 'finance/view_invoice.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def receipt(request):
    if 'read_finance' in custom_data_views(request):
        receipts = Receipt.objects.all()
        searched_receipts = receipts
        query = request.GET.get("query", "")
        if query != "":
            receipts = searched_receipts.filter(Q(id__icontains=query))

        all_receipts = Receipt.objects.all()

        receipt_summary = 0
        for all_receipts in all_receipts:
            receipt_summary = receipt_summary+all_receipts.paid_amount

        context = {
            'query': query,
            'id': id,
            'receipt_summary': receipt_summary,
            'receipts': receipts,
        }
        return render(request, 'finance/receipts.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_receipt(request):
    if 'create_finance' in custom_data_views(request):
        if request.method == "POST":
            student = request.POST["student"]
            payment_method = request.POST["payment_method"]
            paid_amount = request.POST["paid_amount"]
            remarks = request.POST["remarks"]
            if request.FILES and request.FILES["payment_receipt"]:
                payment_receipt = request.FILES["payment_receipt"]
            else:
                payment_receipt = None

            student = Student.objects.get(id=student)
            created_by_user = User.objects.get(username=request.user)

            created_by = str(created_by_user)
            receipt_1 = Receipt.objects.create(student=student, payment_method=payment_method, paid_amount=paid_amount,
                                            payment_receipt=payment_receipt, remarks=remarks, created_by = created_by)
            receipt_1.save()
            details = receipt_1.id
            details = "REC_NO_"+str(details)

            bal = Statement.objects.filter(student=student).order_by('-id')[:1].get()
            initial_balance = bal.balance
            balance = float(initial_balance) - float(paid_amount)
            Statement.objects.create(student=student, transaction='receipt',
                                    details=details, payment=paid_amount, balance=balance)
            return redirect(single_statement, id=student.id)
        else:
            student = Student.objects.all()
            context = {
                'student': student
            }
            return render(request, "finance/create_receipt.html", context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def view_receipt(request, id):
    if 'read_finance' in custom_data_views(request):
        receipt = Receipt.objects.get(id=id)
        context = {
            'receipt': receipt,
        }
        return render(request, 'finance/view_receipt.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def finance(request):
    if 'read_finance' in custom_data_views(request):
        invoice = Invoice.objects.all()
        receipt = Receipt.objects.all()
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)

        weekly_invoice_total = Invoice.objects.filter(
            created__gte=start_date, created__lte=end_date
        ).aggregate(total=Sum('invoice_amount'))['total'] or 0

        weekly_receipt_total = Receipt.objects.filter(
            created__gte=start_date, created__lte=end_date
        ).aggregate(total=Sum('paid_amount'))['total'] or 0

        weekly_expense_total = Expense.objects.filter(
            created__gte=start_date, created__lte=end_date
        ).aggregate(total=Sum('expense_amount'))['total'] or 0
        
        total_invoice_amt=0
        if invoice:
            for invoice in invoice :
                
                total_invoice_amt = total_invoice_amt+ invoice.invoice_amount


        total_receipt_amt=0
        if receipt:
            for receipt in receipt :
                total_receipt_amt = total_receipt_amt+ receipt.paid_amount

        today = date.today()
        last_7_days = today - timedelta(days=6)
        
        students = Student.objects.all()
        recent_statements = []
        for student in students:
            try:
                recent_statement = Statement.objects.filter(student=student).latest('id')
                recent_statements.append(recent_statement)
            except Statement.DoesNotExist:
                return redirect('home')
        recent_statements = sorted(recent_statements, key=lambda x: x.balance, reverse=True)[:5]

        
        
        day_format = '%B %d'
        context = {
            'totals_by_day': [
                {
                    'date': (last_7_days + timedelta(days=i)).strftime(day_format),
                    'invoice_total': Invoice.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('invoice_amount'))['total'] or 0,
                    'receipt_total': Receipt.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('paid_amount'))['total'] or 0,
                    'expense_total': Expense.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=Sum('expense_amount'))['total'] or 0,
                }
                for i in range(7)
            ],
            'total_invoice_amt':total_invoice_amt,
            'total_receipt_amt':total_receipt_amt,
            'weekly_invoice_total':weekly_invoice_total,
            'weekly_receipt_total':weekly_receipt_total,
            'weekly_expense_total':weekly_expense_total,
            'recent_statements': recent_statements,
        }
        return render (request, 'finance/dashboard.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

 
def single_statement(request, id):
    if 'read_finance' in custom_data_views(request):
        statements = Statement.objects.filter(student=id)

        calc_statements = Statement.objects.filter(student=id)
        amt_total = 0.0
        for calc_statements in calc_statements:
            if type(calc_statements.amount) is float:
                amt_total = amt_total+calc_statements.amount

        calc_statements_2 = Statement.objects.filter(student=id)
        total_payment = 0.0
        for calc_statements_2 in calc_statements_2:
            if type(calc_statements_2.payment) is float:
                total_payment = total_payment+calc_statements_2.payment

        balance_due = amt_total-total_payment

        student = Student.objects.get(id=id)
        context = {
            'student': student,
            'balance_due': balance_due,
            'statements': statements,
        }
        return render(request, 'finance/single_statement.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def expenses(request):
    if 'read_finance' in custom_data_views(request):
        expense = Expense.objects.all()
        expense_type= ExpenseType.objects.all()
        
        context = {
            'expense': expense,
            'expense_type': expense_type,
        }
        return render(request, 'finance/expenses.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def create_expense(request):
    if 'read_finance' in custom_data_views(request):
        if request.method == "POST":
            expense_title = request.POST['expense_title']
            expense_amount  = request.POST['expense_amount']
            type = request.POST['expense_type']
            remarks = request.POST['remarks']

            expense_type = ExpenseType.objects.get(id=type)
            Expense.objects.create(expense_title = expense_title, expense_amount = expense_amount, 
                                   expense_type = expense_type,remarks = remarks)
            return redirect('expenses')
        else:
            
            return render(request, 'finance/expenses.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def edit_expense(request,id):
    if 'update_finance' in custom_data_views(request):
        if request.method =="POST":
            expense_type = request.POST['expense_type']
            expense_title = request.POST['expense_title']
            expense_amount = request.POST['expense_amount']
            expense_remarks = request.POST['expense_remarks']

            expense_obj = Expense.objects.get(id=id)
            exp_type = ExpenseType.objects.get(id=expense_type)
            expense_obj.expense_type = exp_type
            expense_obj.expense_title = expense_title
            expense_obj.expense_amount = expense_amount
            expense_obj.remarks = expense_remarks
            expense_obj.save()

            return redirect('expenses')
        else:
            expense = Expense.objects.get(id=id)
            expense_type = ExpenseType.objects.all()
            context = {
                'expense_type':expense_type,
                'expense':expense
            }
            return render(request,'finance/edit_expense.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
            
    
def delete_expense(request,id):
    if 'update_finance' in custom_data_views(request):
        expense = Expense.objects.get(id=id)
        expense.delete()
        return redirect('expenses')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def finance_setup(request):
    if 'manage_finance' in custom_data_views(request):
        expense_type  = ExpenseType.objects.all()
        context = {
            'expense_type':expense_type
        }
        return render (request,'finance/finance_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_expense_type(request):
    if 'create_finance' in custom_data_views(request):
        if request.method =="POST":
            expense_type = request.POST['expense_type']
            ExpenseType.objects.create(expense_type =expense_type)
            return redirect('finance_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')   


def delete_expense_type(request,id):
    if 'create_finance' in custom_data_views(request):
        expense_type = ExpenseType.objects.get(id=id)
        expense_type.delete()
        return redirect('finance_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')   



def edit_expense_type(request,id):
    if 'update_finance' in custom_data_views(request):
        if request.method =="POST":
            expense_type = request.POST['expense_type']
            expense_obj = ExpenseType.objects.get(id=id)
            expense_obj.expense_type = expense_type
            expense_obj.save()
            return redirect('finance_setup')
        else:
            expense_type = ExpenseType.objects.get(id=id)
            context = {
                'expense_type':expense_type
            }
            return render(request,'finance/edit_expense_type.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')  
