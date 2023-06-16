from django.shortcuts import render,redirect
from .models import *
from features.models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from datetime import date,datetime,timedelta
from django.core.paginator import Paginator
from account.context_processors import custom_data_views
# Create your views here.
from django.db.models import Count
from zk import ZK, const
from datetime import datetime
from datetime import date
from django.utils.timezone import make_aware
from datetime import date
from django.db import transaction



def hrm_setup(request):
    if 'read_hrm' in custom_data_views(request):
        months = MonthSetup.objects.all()

    # Create a list of dictionaries with month details and holiday count
        month_list = []
        for month in months:
            holidays = month.holidays.all()
            holiday_count = holidays.count()
            month_dict = {
                'month': month,
                'holidays': holidays,
                'holiday_count': holiday_count,
            }
            month_list.append(month_dict)

            
        holidays = Holidays.objects.all()
        year = YearSetup.objects.all()
        department = Department.objects.all()
        designation = Designation.objects.all()


        if DeviceData.objects.all().exists():
            device_data = DeviceData.objects.order_by('created')[0]
            can_add = False
        else:
            device_data = None
            can_add = True
        
        context = {
            'month_list':month_list, 
            'holidays':holidays, 
            'year':year,
            'department':department, 
            'designation':designation,
            'device_data':device_data,
            'can_add':can_add,
        }
        return render (request,'hrm/hrm_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_year(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            year = request.POST['year']
            if YearSetup.objects.filter(year=year).exists():
                messages.info(request, "Year already exixts")
                return redirect(hrm_setup)
            else:
                YearSetup.objects.create(year=year)
                messages.info(request, "Year Added Successfully")
                return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def edit_year(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            year = request.POST['year']
            year_obj = YearSetup.objects.get(id=id)
            year_obj.year=year
            year_obj.save()
            messages.info(request, "Year Edited Successfully")
            return redirect(hrm_setup)
        else:
            year_data = YearSetup.objects.get(id=id)
            context= {
                'year_data':year_data,
            }
            return render(request,'hrm/edit_year.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_year(request,id):
    if 'delete_hrm' in custom_data_views(request):
        year = YearSetup.objects.get(id=id)
        year.delete()
        messages.info(request, "Year Deleted")
        return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

    

def add_month(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            year = request.POST['year']
            month = request.POST['month']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            holidays = request.POST['holidays']

            year = YearSetup.objects.get(id=year)
            month = MonthSetup.objects.create(year=year,month=month,start_date=start_date,end_date=end_date)
            month.save()
            date_list = [date.strip() for date in holidays.split(",")]
            for holiday in date_list:
                Holidays.objects.create(month = month, holiday = holiday)

            messages.info(request, "Year Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def edit_month(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            year = request.POST['year']
            month = request.POST['month']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            holidays = request.POST['holidays']
            is_active = request.POST.get('is_active', 0)
            year = YearSetup.objects.get(id=year)

            month_obj = MonthSetup.objects.get(id=id)
            month_obj.year=year
            month_obj.month=month
            month_obj.start_date=start_date
            month_obj.end_date=end_date
            month_obj.is_active=is_active
            month_obj.save()

            prev_holidays = Holidays.objects.filter(month=id)
            prev_holidays.delete()
            date_list = [date.strip() for date in holidays.split(",")]
            for holiday in date_list:
                Holidays.objects.create(month = month_obj, holiday = holiday)

            messages.info(request, "Year Edited Successfully")
            return redirect(hrm_setup)
        else:
            year = YearSetup.objects.all()
            month_data = MonthSetup.objects.get(id=id)
            print(month_data.is_active)
            month_holidays = Holidays.objects.filter(month = month_data.id)
            context= {
                'year':year,
                'month_data':month_data,
                'month_holidays':month_holidays,
            }
            return render(request,'hrm/edit_month.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_month(request,id):
    if 'delete_hrm' in custom_data_views(request):
        month = MonthSetup.objects.get(id=id)
        month.delete()
        messages.info(request, "Month Deleted")
        return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    



def add_department(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            department = request.POST['department']
            Department.objects.create(department=department)
            messages.info(request, "Department Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_department(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            department = request.POST['department']
            department_obj = Department.objects.get(id=id)

            department_obj = Department.objects.get(id=id)
            department_obj.department=department
            department_obj.save()
            messages.info(request, "Department Edited Successfully")
            return redirect(hrm_setup)
        else:
            department_data = Department.objects.get(id=id)
            context= {
                'department_data':department_data,
            }
            return render(request,'hrm/edit_department.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_department(request,id):
    if 'delete_hrm' in custom_data_views(request):
        department = Department.objects.get(id=id)
        employee = Employee.objects.filter(department=department)
        if employee:
            messages.info(request, "Assign employees to another department to delete this department.")
            return redirect('hrm_setup')
        else:
            department.delete()
            messages.info(request, "Department Deleted")
            return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def add_designation(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            department = request.POST['department']
            designation = request.POST['designation']
            department = Department.objects.get(id=department)
            Designation.objects.create(department=department,designation=designation)
            messages.info(request, "Designation Added Successfully")
            return redirect(hrm_setup)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_designation(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method == 'POST':
            department = request.POST['department']
            designation = request.POST['designation']
            department = Department.objects.get(id=department)

            designation_obj = Designation.objects.get(id=id)
            designation_obj.department=department
            designation_obj.designation=designation
            designation_obj.save()
            messages.info(request, "Designation Edited Successfully")
            return redirect(hrm_setup)
        else:
            department = Department.objects.all()
            designation_data = Designation.objects.get(id=id)
            context= {
                'designation_data':designation_data,
                'department':department,
            }
            return render(request,'hrm/edit_designation.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_designation(request,id):
    if 'delete_hrm' in custom_data_views(request):
        designation = Designation.objects.get(id=id)
        employee = Employee.objects.filter(designation=designation)
        if employee:
            messages.info(request, "Assign employees to another designation to delete this designation.")
            return redirect('hrm_setup')
        else:
            designation.delete()
            messages.info(request, "Designation Deleted")
            return redirect('hrm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def employee_dashboard(request):
    employees = Employee.objects.all()
    context = {
        'employees':employees,
    }
    return render (request,'hrm/dashboard.html',context)
    

def employees(request):
    if 'read_hrm' in custom_data_views(request):
        employees = Employee.objects.all()
        context = {
            'employees':employees,
        }
        return render (request,'hrm/employees.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def add_employee(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method=="POST":
            designation = request.POST['designation']
            department = request.POST['department']
            contact = request.POST['contact']
            address = request.POST['address']
            salary = request.POST['salary']
            date_joined = request.POST['date_joined']
            

            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            role = request.POST['role']

            pass_obj= password
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            permission=Permission.objects.get(role=role)
            designation = Designation.objects.get(id=designation)
            department = designation.department
            
            Employee.objects.create(user=user,emp_password=pass_obj,permission=permission,designation =designation,department =department,email =email,contact =contact,address =address,emp_salary =salary,date_joined = date_joined)
            messages.info(request, "Employee Added Successfully")

            return redirect('employees')
        else:
            designation = Designation.objects.all()
            department = Department.objects.all()
            roles = Role.objects.all()
            context = {
            'roles':roles,
            'designation':designation,
            'department':department,
        }
            return render(request,'hrm/add_employee.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_employee(request,id):
    if 'update_hrm' in custom_data_views(request):
        if request.method =="POST":
            designation = request.POST['designation']
            department = request.POST['department']
            contact = request.POST['contact']
            address = request.POST['address']
            salary = request.POST['salary']
            date_joined = request.POST.get('date_joined', '')
            
            password = request.POST['password']
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            role = request.POST['role']
            pass_obj= password


            user_data = Employee.objects.get(id=id)
            permission=Permission.objects.get(role=role)
            department=Department.objects.get(id=department)
            designation=Designation.objects.get(id=designation)

            emp_user = user_data.user
            user=User.objects.get(username = emp_user)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            if password:
                user.set_password(password)
            user.save()

            user_data.permission=permission
            user_data.designation = designation
            user_data.department = department
            user_data.contact = contact
            user_data.address = address
            user_data.emp_salary = salary
            user_data.email = email
            if password:
                user_data.emp_password=pass_obj
            if date_joined:
                user_data.date_joined = date_joined
            user_data.save()
            messages.info(request, "Employee Edited Successfully.")
            return redirect('employees')
        else:
            user_data = Employee.objects.get(id=id)
            designation = Designation.objects.all()
            department = Department.objects.all()
            roles = Role.objects.all()
            context={
                'user_data':user_data,
                'roles':roles,
                'designation':designation,
                'department':department,
            }
            return render (request,'hrm/edit_employees.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_employee(request,id):
    if 'delete_hrm' in custom_data_views(request):
        employee = Employee.objects.get(id=id)
        payments_made = Salary.objects.filter(employee=employee )
        context = {
            'employee':employee,
            'payments_made':payments_made,
            }
        return render(request,'hrm/view_employee.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
    
def delete_employee(request,id):
    if 'delete_hrm' in custom_data_views(request):
        user_data = Employee.objects.get(id=id)
        user = User.objects.get(username=user_data.user.username)
        print(user)
        if (user.is_superuser==True):
            messages.info(request, "This user can't be deleted.")
        else:
            user.delete()
            user_data.delete()
            messages.info(request, "User Deleted Successfully")
        return redirect('employees')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def manage_attendance(request):
    if request.method == "POST":
        today_date = date.today()
        recent_attendance = Attendance.objects.filter(date=today_date).first()
        if recent_attendance:
            with transaction.atomic():
                Attendance.objects.filter(date=today_date).delete()

                status_list = request.POST.getlist("status")
                reason_list = request.POST.getlist("reason")
                employee_list = request.POST.getlist("employee")

                for status, reason, employee_id in zip(status_list, reason_list, employee_list):
                    employee = Employee.objects.get(id=int(employee_id))
                    attendance = Attendance.objects.create(
                        employee=employee,
                        date=today_date,
                        status=status,
                        reason=reason
                    )
                    attendance.save()
                messages.info(request, f"Attendance Updated for today.")
            return redirect('manage_attendance')

        else:
            status_list = request.POST.getlist("status")
            reason_list = request.POST.getlist("reason")
            employee_list = request.POST.getlist("employee")

            for status, reason, employee_id in zip(status_list, reason_list, employee_list):
                employee = Employee.objects.get(id=int(employee_id))
                attendance = Attendance.objects.create(employee=employee,date=today_date,status=status,reason=reason)
                attendance.save()
            messages.info(request, f"Attendance Updated for date:{today_date}")
            return redirect('manage_attendance')

    else:
        today_date=date.today()
        today_attendance = Attendance.objects.filter(date=today_date)
        if today_attendance.exists():
            attendance_object = Attendance.objects.filter(date=today_date)
            status = "taken"
        else:
            attendance_object=None
            status = "not-taken"

        employee=Employee.objects.all()

        context={
            'today_date':today_date,
            'employee':employee,
            'status':status,
            'attendance_object':attendance_object,
        }
        return render(request, 'hrm/attendance.html',context)




