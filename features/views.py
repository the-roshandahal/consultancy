import random
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
from finance.models import *
from features.models import *
from student.models import *
from account.context_processors import *
from datetime import datetime,date,timedelta
import requests


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            active_student_count = Student.objects.filter(active=True).count()
            student_count = Student.objects.all().count()
            invoice_count = Invoice.objects.all().count()
            receipt_count = Receipt.objects.all().count()
            invoice_amount = Invoice.objects.aggregate(sum_amount=models.Sum('invoice_amount'))['sum_amount']
            receipt_amount = Receipt.objects.aggregate(sum_amount=models.Sum('paid_amount'))['sum_amount']
            logged_in_user = User.objects.get(username=request.user)
            try:
                company_user = Employee.objects.get(user=logged_in_user)
            except:
                company_user=None
            incomplete_todo = ToDo.objects.filter(task_to = company_user, status = 'incomplete')[:5]
            incomplete_todo_count = ToDo.objects.filter(task_to = company_user, status = 'incomplete').count()
            


            try:
                random_number = random.randint(0, 1642)
                response = requests.get("https://type.fit/api/quotes")
                data = response.json()
                random_quote = data[random_number]['text']
                author = data[random_number]['author'] if data[random_number]['author'] else 'Unknown'
            except:
                random_quote = "No quotes for today"
                author= "Unknown"
                
            today = date.today()
            last_7_days = today - timedelta(days=6)
            day_format = '%B %d'
            context = {
                'totals_by_day': [
                    {
                        'date': (last_7_days + timedelta(days=i)).strftime(day_format),
                        'invoice_total': Invoice.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=models.Sum('invoice_amount'))['total'] or 0,
                        'receipt_total': Receipt.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=models.Sum('paid_amount'))['total'] or 0,
                        'expense_total': Expense.objects.filter(created=last_7_days + timedelta(days=i)).aggregate(total=models.Sum('expense_amount'))['total'] or 0,
                    }
                    for i in range(7)
                ],
                'active_student_count':active_student_count,
                'student_count':student_count,
                'invoice_amount':invoice_amount,
                'receipt_amount':receipt_amount,
                'receipt_count':receipt_count,
                'invoice_count':invoice_count,
                "incomplete_todo":incomplete_todo,
                "incomplete_todo_count":incomplete_todo_count,
                'random_quote':random_quote,
                'author':author,
            }
        else:
            return redirect('student_dashboard')

        return render (request,'index.html',context) 
    else:
        return redirect('login')
    





def company_setup(request):
    if 'manage_company' in custom_data_views(request):
        company_setup= Company.objects.all().order_by('-created').first()
        context = {
            'company_setup':company_setup,
        }
        return render (request,'features/company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    




def add_company_setup(request):
    if 'manage_company' in custom_data_views(request):
        if Company.objects.all().exists():
            messages.info(request, "You have already added a setup.")
            return redirect('company_setup')
        else:
            if request.method=='POST':
                company_name = request.POST['company_name']
                company_address = request.POST['company_address']
                company_email = request.POST['company_email']
                company_contact_number = request.POST['company_contact_number']
                company_logo = request.FILES['company_logo']
                payment_terms = request.POST['payment_terms']

                Company.objects.create(company_name = company_name,company_address = company_address,
                                    company_email = company_email,company_contact_number = company_contact_number,company_logo = company_logo,
                                    payment_terms = payment_terms)
                messages.info(request, "Company details added successfully.")
                
                return redirect('company_setup')
            else:
                return render(request,'features/add_company_setup.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def edit_company_setup(request,id):
    if 'manage_company' in custom_data_views(request):
        if request.method=='POST':
            setup = Company.objects.get(id=id)
            setup.company_name = request.POST['company_name']
            setup.company_address = request.POST['company_address']
            setup.company_email = request.POST['company_email']
            setup.company_contact_number = request.POST['company_contact_number']
            setup.payment_terms = request.POST['payment_terms']

            if request.FILES and request.FILES['company_logo']:
                setup.company_logo = request.FILES['company_logo']
            setup.save()
            messages.info(request, "Company details edited successfully.")

            return redirect('company_setup')
        else:
            setup = Company.objects.get(id=id)
            print(setup.company_name)
            context = {
            'setup':setup
            }
            return render(request,'features/edit_company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
  


   
def todo(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users = Employee.objects.all()
            context = {
                'users':users,
            }
            return render (request, 'features/todo.html',context)
        else:
            logged_in_user = User.objects.get(username=request.user)
            company_user = Employee.objects.get(user=logged_in_user)

            completed_todo = ToDo.objects.filter(task_to = company_user, status = 'completed')
            incomplete_todo = ToDo.objects.filter(task_to = company_user, status = 'incomplete')
            reassigned_todo = ToDo.objects.filter(task_to = company_user, status = 'reassigned')

            mytasks = ToDo.objects.filter(task_from= company_user)
            
            users = Employee.objects.all()
            print(company_user)
            context = {
                'reassigned_todo':reassigned_todo,
                'completed_todo':completed_todo,
                'incomplete_todo':incomplete_todo,
                'mytasks':mytasks,
                'users':users,
                'company_user':str(company_user)
            }
            return render (request, 'features/todo.html',context)


def add_todo(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages.info(request, "Superuser can't add tasks. Please use your employee account to continue.")

            return redirect(todo)
        else:
            if request.method == "POST":
                task_title = request.POST["task_title"]
                task = request.POST["task"]
                deadline = request.POST["deadline"]
                priority = request.POST["priority"]
                assign_to = request.POST.getlist("assign_to")


                logged_in_user = User.objects.get(username=request.user)
                task_from = Employee.objects.get(user=logged_in_user)
                for assign_to in assign_to:
                    assign_to = Employee.objects.get(id=assign_to)
                    
                    todo_obj = ToDo.objects.create(task_title=task_title,task=task,deadline=deadline,priority=priority,task_to=assign_to,task_from=str(task_from))
                    todo_obj.save()
                    
                    notification_obj = f"{task_from} assigned you a task - {task_title}."
                    notification = EmployeeNotification.objects.create(employee = assign_to,notification=notification_obj)
                    notification.save()
    
                messages.info(request, "Task added successfully.")

                return redirect('todo')
            return redirect ('todo')


def change_status(request,id):
    if request.user.is_authenticated:
        todo_data = ToDo.objects.get(id=id)
        if todo_data.status == 'incomplete':
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "completed"
            status_update.save()
            messages.info(request, "Status Changed to completed")
            return redirect(todo)

        elif todo_data.status =='reassigned':
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "completed"
            status_update.save()
            messages.info(request, "Status Changed to completed")
            return redirect(todo)

        else:
            status_update = ToDo.objects.filter(id=id)[0]
            status_update.status = "incomplete"
            status_update.save()
            messages.info(request, "Status Changed to Incomplete")
            return redirect(todo)

def reassign(request,id):
    if request.user.is_authenticated:
        status_update = ToDo.objects.filter(id=id)[0]
        status_update.status = "reassigned"
        status_update.save()
        messages.info(request, "Status Changed to Resassigned")
        return redirect(todo)




def mark_all_as_read(request):
    if request.user.is_authenticated:
        try:
            logged_in_user = User.objects.get(username=request.user)
            employee = Employee.objects.get(user=logged_in_user)
            unread_notifications = EmployeeNotification.objects.filter(employee=employee,status="unread")
            for notification in unread_notifications:
                notification.status = "read"
                notification.save()
            messages.info(request,"Marked successfully.")
            return redirect('home')
        except:
            messages.info(request,"Error encountered.")
            return redirect('home')
    else:
        messages.info(request,"Unauthorized access.")
        return redirect('home')
    

from django.shortcuts import render

def error_404(request, exception):
    return render(request, 'error.html', status=404)


def error_500(request):
    return render(request, 'error.html', status=500)
