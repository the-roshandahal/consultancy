from django.shortcuts import render,redirect
from .models import *
from features.models import *
from finance.models import *
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from datetime import date,datetime,timedelta
from django.core.paginator import Paginator
from account.context_processors import custom_data_views
# Create your views here.
from django.db.models import Count
# from zk import ZK, const
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
            month_dict = {
                'month': month,
            }
            month_list.append(month_dict)

            
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

            year = YearSetup.objects.get(id=year)
            month = MonthSetup.objects.create(year=year,month=month,start_date=start_date,end_date=end_date)
            month.save()

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
            is_active = request.POST.get('is_active', 0)
            year = YearSetup.objects.get(id=year)

            month_obj = MonthSetup.objects.get(id=id)
            month_obj.year=year
            month_obj.month=month
            month_obj.start_date=start_date
            month_obj.end_date=end_date
            month_obj.is_active=is_active
            month_obj.save()

            messages.info(request, "Year Edited Successfully")
            return redirect(hrm_setup)
        else:
            year = YearSetup.objects.all()
            month_data = MonthSetup.objects.get(id=id)
            print(month_data.is_active)
            context= {
                'year':year,
                'month_data':month_data,
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

def leave(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = {
            }
            return render (request,'hrm/leave.html',context)
        else:
            employee = Employee.objects.get(user=request.user)
            approved_leaves = Leave.objects.filter(employee=employee)
            approved_leave_dates = LeaveDate.objects.filter(leave__in=approved_leaves)
            context = {
                'approved_leaves':approved_leaves,
                'approved_leave_dates':approved_leave_dates
                }
            return render (request,'hrm/leave.html',context)

def apply_leave(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            reason = request.POST['reason']
            dates = request.POST['dates']
            employee = Employee.objects.get(user=request.user)
            leave = Leave.objects.create(reason=reason,status='pending',employee=employee)
            leave.save()
            date_list= [date.strip() for date in dates.split(",")]
            for date in date_list:
                LeaveDate.objects.create(leave=leave,date=date)

            return redirect('leave')
        else:
            return render (request,'hrm/apply_leave.html')
def emp_leaves(request):
    if 'read_hrm' in custom_data_views(request):
        pending_leaves = Leave.objects.filter(status='pending')
        pending_leaves_dates = LeaveDate.objects.filter(leave__in=pending_leaves)

        approved_leaves = Leave.objects.filter(status='accepted')
        approved_leaves_dates = LeaveDate.objects.filter(leave__in=approved_leaves)
        
        denied_leaves = Leave.objects.filter(status='denied')
        denied_leaves_dates = LeaveDate.objects.filter(leave__in=denied_leaves)

        context = {
            'pending_leaves':pending_leaves,
            'pending_leaves_dates':pending_leaves_dates,

            'approved_leaves':approved_leaves,
            'approved_leaves_dates':approved_leaves_dates,
            
            'denied_leaves':denied_leaves,
            'denied_leaves_dates':denied_leaves_dates,
        }
        return render (request,'hrm/emp_leaves.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def add_emp_leave(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method=="POST":
            emp = request.POST['employee']
            reason = request.POST['reason']
            days = request.POST['dates']
            employee = Employee.objects.get(id=emp)
            date_list = [date.strip() for date in days.split(",")]
            leave = Leave.objects.create(reason=reason,status='accepted',employee=employee)
            leave.save()
            for date in date_list:
                LeaveDate.objects.create(leave=leave,date=date)
            return redirect('emp_leaves')
        else:
            employees =Employee.objects.all()

            context={
            'employees':employees,

            }
            return render (request,'hrm/add_emp_leave.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def accept_leave(request,id):
    if 'update_hrm' in custom_data_views(request):
        leave = Leave.objects.get(id=id)
        leave.status = 'accepted'
        leave.save()
        return redirect('emp_leaves')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def deny_leave(request,id):
    if 'update_hrm' in custom_data_views(request):
        leave = Leave.objects.get(id=id)
        leave.status = 'denied'
        leave.save()
        return redirect('emp_leaves')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')





def payroll(request):
    if 'read_hrm' in custom_data_views(request):
        months = MonthSetup.objects.filter(is_active = True)      
        current_datetime = date.today()
        date_object = current_datetime
        today_date = date_object.strftime('%Y-%m-%d')
        all_employees = Employee.objects.all()
        recent_salary = Salary.objects.all().order_by('created')
        

        # paginator = Paginator(recent_salary, 10)
        # page_number = request.GET.get('page')
        # recent_salary = paginator.get_page(page_number)
        context = {
            'months':months,
            'today_date':today_date,
            'all_employees':all_employees,
            'recent_salary':recent_salary,
        }
        return render(request,'hrm/payroll.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def advance_salary(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            month = request.POST['month']
            employee = request.POST['employee']
            amount = request.POST['amount']
            type='advance'
            leave_deduction=0
            tax_deduction=0
            employee=Employee.objects.get(id=employee)
            sel_month=MonthSetup.objects.get(month=month)
            salary_obj = Salary.objects.filter(employee=employee,month=sel_month,type='salary')
            if salary_obj:
                messages.info(request, "You have already paid the salary of this employee for this month. Please select another month for advance payment.")
            else:
                Salary.objects.create(employee=employee,month=sel_month,paid_salary=amount,type=type,leave_deduction=leave_deduction,tax_deduction=tax_deduction)
                messages.info(request, "Advance issued successfully.")

            return redirect('payroll')
        else:
            return redirect('payroll')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def salary_payment(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method == "POST":
            month = request.POST['month']
            employee = request.POST['employee']
            type = 'salary'
            leave_deduction = 0
            tax_deduction = 0
            employee = Employee.objects.get(id=employee)
            sel_month = MonthSetup.objects.get(month=month)
            salary_obj = Salary.objects.filter(employee=employee, month=sel_month, type='salary')
            if salary_obj:
                messages.info(request, "You have already paid the salary of this employee for this month. Please select another month.")
            else:
                Salary.objects.create(employee=employee, month=sel_month, type=type, leave_deduction=leave_deduction, tax_deduction=tax_deduction)
                messages.info(request, "Salary paid successfully.")
            return redirect('payroll')
        else:
            all_employees = Employee.objects.all()
            months = MonthSetup.objects.all()
            context = {
                        'months':months,
                        'all_employees':all_employees,
                    }
            return render(request,'hrm/payroll.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def salary_payment(request):
    if 'read_hrm' in custom_data_views(request):
        if request.method =="POST":
            month = request.POST['month']
            selected_month = MonthSetup.objects.get(id=month)
            start_date = selected_month.start_date
            end_date = selected_month.end_date

            data_list=[]

            all_emp = Employee.objects.all()

            for emp_to_pay in all_emp:
                
                leaves = Leave.objects.filter(employee = emp_to_pay,status='accepted',created__range=(start_date, end_date))
                absent_days = 0
                leave_days =[]
                for leave in leaves:
                    leave_dates = LeaveDate.objects.filter(leave=leave)
                    for leave_date in leave_dates:
                        if start_date <= leave_date.date <= end_date:
                            absent_days += 1
                            leave_days.append(leave_date.date)

                
                total_month_dates = end_date-start_date
                diff = total_month_dates.days+1
                payable_days = diff-len(leave_days)

                salary=emp_to_pay.emp_salary
                emp_daily_salary = int(salary)/diff
                salary_to_pay = emp_daily_salary*payable_days


                
                if salary_to_pay <= 41666.66:
                    tax_deduction = salary_to_pay * 0.01
                elif salary_to_pay <= 58333.33:
                    tax_deduction = 500 + (salary_to_pay - 41666.66) * 0.1
                elif salary_to_pay <= 83333.33:
                    tax_deduction = 2500 + (salary_to_pay - 58333.33) * 0.2
                elif salary_to_pay <= 166666.67:
                    tax_deduction = 6500 + (salary_to_pay - 83333.33) * 0.3
                else:
                    tax_deduction = 24166.67 + (salary_to_pay - 166666.67) * 0.36



                leave_deduction = len(leave_days) * emp_daily_salary
                advance_this_month =0
                advance_obj = Salary.objects.filter(employee = emp_to_pay,type='advance',month=selected_month)
                for adv in advance_obj:
                    advance_this_month = advance_this_month + adv.paid_salary

                final_salary = salary_to_pay-tax_deduction-leave_deduction-advance_this_month
                salary_status = Salary.objects.filter(employee = emp_to_pay,month=selected_month,type='salary')
                if salary_status:
                    status='paid'
                else:
                    status='unpaid'
                
                data_list.append({
                    'emp_id':emp_to_pay,
                    'month':selected_month.month,
                    'employee':str(emp_to_pay.user.first_name +' '+ emp_to_pay.user.last_name),
                    'absent_days':absent_days,
                    'payable_days':payable_days,
                    'salary':salary,
                    'final_salary':final_salary,
                    'tax_deduction':tax_deduction,
                    'leave_deduction':leave_deduction,
                    'status':status,
                    'advance_this_month':advance_this_month
                })
            context = {
                'data_list':data_list,
                'month':selected_month.month,
            }
        return render(request,'hrm/salary_payment.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def pay_salary(request):
    if 'create_hrm' in custom_data_views(request):
        if request.method =="POST":
            selected_employees = request.POST.getlist("selected_employees")
            leave_deduction = request.POST.getlist("leave_deduction")
            tax_deduction = request.POST.getlist("tax_deduction")
            final_salary = request.POST.getlist("final_salary")
            month = request.POST["month"]
            print(month)
            company_deduction = request.POST.getlist("company_deduction")
            for i in range(len(selected_employees)):
                employee=Employee.objects.get(id=selected_employees[i])
                month=MonthSetup.objects.get(month=month)
                salary = Salary.objects.create(
                    employee=employee,
                    month=month,
                    leave_deduction=leave_deduction[i],
                    tax_deduction=tax_deduction[i],
                    company_deduction=company_deduction[i],
                    paid_salary=final_salary[i],
                    type='salary',
                )
                salary.save()
            return redirect('payroll')      
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
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username,is_staff=True)
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
            status = "Taken"
        else:
            attendance_object=None
            status = "Not taken"
        latest = Attendance.objects.latest('last_updated')
        last_updated=latest.last_updated
        employee=Employee.objects.all()

        context={
            'today_date':today_date,
            'employee':employee,
            'status':status,
            'last_updated':last_updated,
            'attendance_object':attendance_object,
        }
        return render(request, 'hrm/attendance.html',context)



def attendance_history(request):
    if 'manage_hrm' in custom_data_views(request):
        if request.method =="POST":
            to_date = request.POST['to_date']
            from_date = request.POST['from_date']
            employee_ids = request.POST['employees']
            if employee_ids == "all":
                attendance = Attendance.objects.filter(
                    date__range=[from_date, to_date])
            else:
                attendance = Attendance.objects.filter(
                    date__range=[from_date, to_date],
                    employee__id__in=employee_ids
                )

            employees = Employee.objects.all()
            context={
                'attendance':attendance,
                'employees':employees,
            }
        else:
            employees = Employee.objects.all()
            attendance= Attendance.objects.all()
            context={
                'attendance':attendance,
                'employees':employees,
            }
        return render(request,'hrm/attendance_history.html',context)
    

def payslip(request):
    if request.user.is_superuser:
        context = {
        }
        return render(request,'hrm/payslip.html',context)
    else:
        employee = Employee.objects.get(user=request.user)
        payments_made = Salary.objects.filter(employee=employee )
        context = {
            'payments_made':payments_made,
            }
        return render(request,'hrm/payslip.html',context)
