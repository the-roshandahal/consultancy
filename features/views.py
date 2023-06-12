from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
from account.context_processors import *

# def homepage(request):
#     if request.user.is_authenticated:
#         return redirect('home') 
#     else:
#         return render (request,'homepage.html')

def home(request):
    if request.user.is_authenticated:
        return render (request,'index.html') 
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
            setup.payment_details = request.POST['payment_details']

            if request.FILES and request.FILES['company_logo']:
                setup.company_logo = request.FILES['company_logo']
            setup.save()
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
                print('here')
                task_title = request.POST["task_title"]
                task = request.POST["task"]
                deadline = request.POST["deadline"]
                priority = request.POST["priority"]
                assign_to = request.POST.getlist("assign_to")


                logged_in_user = User.objects.get(username=request.user)
                task_from = Employee.objects.get(user=logged_in_user)
                for assign_to in assign_to:
                    assign_to = Employee.objects.get(id=assign_to)
                    print(assign_to)
                    todo_obj = ToDo.objects.create(task_title=task_title,task=task,deadline=deadline,priority=priority,task_to=assign_to,task_from=task_from)
                    print(todo_obj)
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

