from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .models import *
from hrm.models import *
from student.models import *
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .context_processors import custom_data_views
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user is None:
                messages.info(request, "Invalid credentials")
                return redirect("login")
                
            if user is not None and user.is_superuser:
                auth.login(request, user)
                messages.info(request, "Logged in successfully.")
                return redirect('home')
                # return redirect("admin:index")

            if user is not None:
                if Employee.objects.filter(user=user).exists():
                    auth.login(request, user)
                    messages.info(request, "Logged in as employee successfully.")
                    return redirect('home')

                
                if Student.objects.filter(user=user).exists():
                    if Student.objects.filter(log=True):
                        auth.login(request, user)
                        messages.info(request, "Logged in as student successfully.")
                        return redirect('student_dashboard')
                    else:
                        messages.info(request, "Cant login to the system.")
                        return redirect('login')

            if user is not None:
                auth.login(request, user)
                messages.info(request, "Logged in successfully.")
                return redirect('home')  
        else:
            return render (request,'account/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect(login)



def role(request):
    if 'read_account' in custom_data_views(request):
        roles = Permission.objects.all()
        context = {
            'roles':roles,
        }
        return render (request,'account/role.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def create_role(request):
    if 'create_account' in custom_data_views(request):
        if request.method == "POST":
            role = request.POST["role"]
            create_finance = request.POST.get('create_finance', 0)
            read_finance = request.POST.get('read_finance', 0)
            update_finance = request.POST.get('update_finance', 0)
            delete_finance = request.POST.get('delete_finance', 0)
            manage_finance = request.POST.get('manage_finance', 0)

            create_account = request.POST.get('create_account', 0)
            read_account = request.POST.get('read_account', 0)
            update_account = request.POST.get('update_account', 0)
            delete_account = request.POST.get('delete_account', 0)
            manage_account = request.POST.get('manage_account', 0)

            create_leads = request.POST.get('create_leads', 0)
            read_leads = request.POST.get('read_leads', 0)
            update_leads = request.POST.get('update_leads', 0)
            delete_leads = request.POST.get('delete_leads', 0)
            manage_leads = request.POST.get('manage_leads', 0)

            create_hrm = request.POST.get('create_hrm', 0)
            read_hrm = request.POST.get('read_hrm', 0)
            update_hrm = request.POST.get('update_hrm', 0)
            delete_hrm = request.POST.get('delete_hrm', 0)
            manage_hrm = request.POST.get('manage_hrm', 0)

            create_course = request.POST.get('create_course', 0)
            read_course = request.POST.get('read_course', 0)
            update_course = request.POST.get('update_course', 0)
            delete_course = request.POST.get('delete_course', 0)
            manage_course = request.POST.get('manage_course', 0)

            create_student = request.POST.get('create_student', 0)
            read_student = request.POST.get('read_student', 0)
            update_student = request.POST.get('update_student', 0)
            delete_student = request.POST.get('delete_student', 0)
            manage_student = request.POST.get('manage_student', 0)
            
            
            create_inquiry = request.POST.get('create_inquiry', 0)
            read_inquiry = request.POST.get('read_inquiry', 0)
            update_inquiry = request.POST.get('update_inquiry', 0)
            delete_inquiry = request.POST.get('delete_inquiry', 0)
            manage_inquiry = request.POST.get('manage_inquiry', 0)



            manage_company = request.POST.get('manage_company', 0)
            try:
                new_role=Role.objects.create( role = role)
                new_role.save()

                role_obj = Role.objects.get(role=new_role)

                Permission.objects.create(role=role_obj,
                                        create_finance =create_finance, read_finance =read_finance, update_finance =update_finance, delete_finance =delete_finance,manage_finance=manage_finance,
                                        create_account =create_account, read_account =read_account, update_account =update_account, delete_account =delete_account,manage_account=manage_account,
                                        create_hrm =create_hrm, read_hrm =read_hrm, update_hrm =update_hrm, delete_hrm =delete_hrm,manage_hrm=manage_hrm,
                                        create_course =create_course, read_course =read_course, update_course =update_course, delete_course =delete_course,manage_course=manage_course,
                                        create_leads =create_leads, read_leads =read_leads, update_leads =update_leads, delete_leads =delete_leads,manage_leads=manage_leads,
                                        manage_company=manage_company,
                                        create_student =create_student, read_student =read_student, update_student =update_student, delete_student =delete_student,manage_student=manage_student,
                                        create_inquiry =create_inquiry, read_inquiry =read_inquiry, update_inquiry =update_inquiry, delete_inquiry =delete_inquiry,manage_inquiry=manage_inquiry,
                                        )
                messages.info(request, "Role created successfully.")
                return redirect('role')

            except Exception:
                print('something went wrong')
                return redirect('role')
        else:
            return render(request,'account/create_role.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def edit_role(request, id):
    if 'update_account' in custom_data_views(request):
        permission = Permission.objects.get(id=id)
        new_role = Role.objects.get(role = permission.role)
        if request.method == "POST":
            new_role.role = request.POST["role"]
            permission.create_finance = request.POST.get('create_finance', 0)
            permission.read_finance = request.POST.get('read_finance', 0)
            permission.update_finance = request.POST.get('update_finance', 0)
            permission.delete_finance = request.POST.get('delete_finance', 0)
            permission.manage_finance = request.POST.get('manage_finance', 0)


            permission.create_account = request.POST.get('create_account', 0)
            permission.read_account = request.POST.get('read_account', 0)
            permission.update_account = request.POST.get('update_account', 0)
            permission.delete_account = request.POST.get('delete_account', 0)
            permission.manage_account = request.POST.get('manage_account', 0)
            
            permission.create_course = request.POST.get('create_course', 0)
            permission.read_course = request.POST.get('read_course', 0)
            permission.update_course = request.POST.get('update_course', 0)
            permission.delete_course = request.POST.get('delete_course', 0)
            permission.manage_course = request.POST.get('manage_course', 0)

            permission.create_hrm = request.POST.get('create_hrm', 0)
            permission.read_hrm = request.POST.get('read_hrm', 0)
            permission.update_hrm = request.POST.get('update_hrm', 0)
            permission.delete_hrm = request.POST.get('delete_hrm', 0)
            permission.manage_hrm = request.POST.get('manage_hrm', 0)

            permission.create_student = request.POST.get('create_student', 0)
            permission.read_student = request.POST.get('read_student', 0)
            permission.update_student = request.POST.get('update_student', 0)
            permission.delete_student = request.POST.get('delete_student', 0)
            permission.manage_student = request.POST.get('manage_student', 0)
            
            
            permission.create_inquiry = request.POST.get('create_inquiry', 0)
            permission.read_inquiry = request.POST.get('read_inquiry', 0)
            permission.update_inquiry = request.POST.get('update_inquiry', 0)
            permission.delete_inquiry = request.POST.get('delete_inquiry', 0)
            permission.manage_inquiry = request.POST.get('manage_inquiry', 0)

            permission.manage_company = request.POST.get('manage_company', 0)
            try:
                permission.save()
                new_role.save()
            except Exception:
                print('something went wrong')
                return redirect('role')
            messages.info(request, "Role edited successfully.")
            return redirect('role')
        else:
            role_data = Permission.objects.get(id=id)
            context={
                'role_data':role_data,
            }
            return render(request, 'account/edit_role.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def delete_role(request, id):
    if 'delete_account' in custom_data_views(request):
        print(id)
        permission = Permission.objects.get(id=id)
        
        role_data = Role.objects.get(id=permission.role.id)
        employees = Employee.objects.filter(permission=permission).exists()

        if employees:
            messages.info(request, f"Please assign the employees with '{role_data}' role to another role before deleting")
            return redirect('role')
        else:
            deleted_role = role_data.role
            role_data.delete()
            messages.info(request, f"{deleted_role} Deleted Successfully")
            return redirect('role')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def view_role(request,id):
    if 'read_account' in custom_data_views(request):
        role_data = Permission.objects.get(id=id)
        print(role_data)
        context={
                'role_data':role_data,
            }
        return render(request,'account/view_role.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def company_user(request):
    if 'read_account' in custom_data_views(request):
        company_users = Employee.objects.all()
        roles = Role.objects.all()
        context = {
            'company_users':company_users,
            'roles':roles,
        }
        return render (request,'account/company_user.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')







def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "The email address you entered is not registered.")
            return redirect('forgot_password')
        
        employee = Employee.objects.get(user=user)
        from random import randint
        code = randint(100000, 999999)
        employee.code = code
        employee.save()
        
        subject = 'Password reset code'
        message = f'Your password reset code is {code}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "We have sent a password reset code to your email.")
        return redirect('verify_otp', email)
    return render(request, 'account/forgot_password.html')

def verify_otp(request, email):
    if request.method == 'POST':
        code = request.POST.get('code')
        email=email
        user = User.objects.get(email=email)
        
        try:
            employee = Employee.objects.get(user=user,code=code)
            if employee:
                messages.success(request, "OTP verified successfully")
                return redirect(reset_password,email)
        except:
            messages.success(request, "OTP couldn't be verified")
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'account/verify_otp.html',{'email':email})

def reset_password(request, email):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email=email
        

        if password == confirm_password:
            user = User.objects.get(email=email)
            employee = Employee.objects.get(user=user)
            
            user.set_password(password)
            user.save()

            employee.emp_password=password
            employee.save()
            messages.success(request, "Password changed successfully")
            return redirect('login')
        else:
            messages.success(request, "Password do not match.")
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'account/reset_password.html',{'email':email})