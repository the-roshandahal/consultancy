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
from django.utils.timezone import make_aware



def hrm(request):
    if 'read_hrm' in custom_data_views(request):
        stats = []
        employee = Employee.objects.all().count()
        # present_today = LogSheet.objects.filter(created = date.today()).count()
        present_today = LogSheet.objects.filter(created=date.today()) \
                    .values('user') \
                    .annotate(count=Count('id', distinct=True)) \
                    .count()
        absent_today = employee-present_today
        department = Department.objects.all().count()
        stats.append({
                'employee': employee,
                'present_today': present_today,
                'absent_today': absent_today,
                'department': department,
            })
        stats = stats[0]
        print(stats)
        context = {
            'stats':stats,
        }
        return render (request,'hrm/hrm.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


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


def log_sheet(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = {

            }
            return render(request, 'hrm/log_sheet.html', context)
        else:
            logged_in_employee = Employee.objects.get(user=request.user)
            current_log = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).first()
            punched_in = False
            punched_out = False
            today_logs = None
            
            if current_log:
                if current_log.punch_out_time is None:
                    punched_in = True
                else:
                    punched_out = True
                    today_logs = LogSheet.objects.filter(user=logged_in_employee, created=date.today()).order_by('-punch_in_time').first()
            
            time_now = datetime.now().time()
            
            context = {
                'time_now': time_now,
                'today_logs': today_logs,
                'punched_in': punched_in,
                'punched_out': punched_out,
            }
            return render(request, 'hrm/log_sheet.html', context)
    else:
        return redirect('login')


def punch_in(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logged_in = Employee.objects.get(user=request.user)
            today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

            current_date = date.today()
            leave_dates = LeaveDate.objects.filter(date=current_date)
            employees_on_leave = [leave_date.leave.employee for leave_date in leave_dates]

            # employee = Employee.objects.get(id=1)  # Replace with the appropriate employee ID
            is_on_leave = logged_in in employees_on_leave
            if is_on_leave:
                messages.info(request, "You are on leave for today.")
                return redirect('log_sheet')
            else:
                if today_logs.exists():
                    messages.info(request, "You have already punched in for today.")
                    return redirect('log_sheet')
                else:
                    punch = LogSheet(user=logged_in, punch_in_time=datetime.now().time())
                    punch.save()
                    messages.success(request, "Punched in successfully.")
                    return redirect('log_sheet')
        return redirect('log_sheet')


def punch_out(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logged_in = Employee.objects.get(user=request.user)
            today_logs = LogSheet.objects.filter(user=logged_in, created=date.today())

            if today_logs.exists() and today_logs.latest('punch_in_time').punch_out_time:
                # User has already punched out for the day, redirect to punch in page
                messages.info(request, "You have already punched out for today.")
                return redirect('punch_in')
            elif today_logs.exists():
                # Update the latest LogSheet instance with user's tasks, meetings, and remarks and punch out time
                punch = today_logs.latest('punch_in_time')
                punch.punch_out_time = datetime.now().time()
                punch.tasks = request.POST['tasks']
                punch.meetings = request.POST['meetings']
                punch.remarks = request.POST['remarks']
                punch.save()
                messages.success(request, "Punched out successfully.")
                return redirect('punch_in')
            else:
                # User has not punched in for the day, redirect to punch in page
                messages.info(request, "You need to punch in before punching out.")
                return redirect('punch_in')
        return redirect('log_sheet')


def attendance (request):
    if 'read_hrm' in custom_data_views(request):
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            employee_id = request.POST.get('employee')
            start_date=start_date
            end_date=end_date
            if employee_id == 'all':
                att_data = LogSheet.objects.filter(created__range=[start_date, end_date])
            else:
                att_data = LogSheet.objects.filter(user_id=employee_id, created__range=[start_date, end_date])
            employees = Employee.objects.all()
            searched = True
            context = {
            'start_date':start_date,
            'end_date':end_date,
            'att_data':att_data,
            'employees':employees,
            'searched':searched
        }
            return render(request, 'hrm/attendance.html',context)
        else:
            att_data=LogSheet.objects.all()
            employees = Employee.objects.all()
            context = {
                'att_data':att_data,
                'employees':employees
            }
            return render (request, 'hrm/attendance.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')








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
    




