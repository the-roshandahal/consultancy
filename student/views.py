from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages, auth
from account.views import *
from account.models import *
from finance.models import *
from account.context_processors import custom_data_views
from features.models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# Create your views here.

def student_dashboard(request):
    logged_in_user= User.objects.get(username=request.user)
    student = Student.objects.get(user=logged_in_user)
    files = StudentFiles.objects.filter(student=student).order_by('-created')
    invoices = Invoice.objects.filter(student=student)  
    receipts = Receipt.objects.filter(student=student)
    context = {
        'student': student,
        'files':files,
        'invoices':invoices,
        'receipts':receipts,
    }
    return render (request,'student/dashboard.html',context)

def student_view_receipt(request, id):
    receipt = Receipt.objects.get(id=id)
    context = {
        'receipt': receipt,
    }
    return render(request, 'student/student_receipt.html', context)
    

def student_view_invoice(request, id):
    invoice = Invoice.objects.get(id=id)
    course = InvoiceCourse.objects.filter(invoice_id=id)
    context = {
        'course':course,
        'invoice': invoice,
    }
    return render(request, 'student/student_invoice.html', context)
    
def student_statement(request):
    logged_in_user= User.objects.get(username=request.user)
    student = Student.objects.get(user=logged_in_user)
    statements = Statement.objects.filter(student=student)
    calc_statements = Statement.objects.filter(student=student)


    amt_total = 0.0
    for calc_statements in calc_statements:
        if type(calc_statements.amount) is float:
            amt_total = amt_total+calc_statements.amount

    calc_statements_2 = Statement.objects.filter(student=student)
    total_payment = 0.0
    for calc_statements_2 in calc_statements_2:
        if type(calc_statements_2.payment) is float:
            total_payment = total_payment+calc_statements_2.payment

    balance_due = amt_total-total_payment
    context = {
        'student': student,
        'statements': statements,
        'balance_due':balance_due
    }
    return render(request, 'student/student_statement.html', context)
    
def student_setup(request):
    if 'read_student' in custom_data_views(request):
        student_stage = StudentStage.objects.all()
        student_source = StudentSource.objects.all()
        enrollment_type = EnrollmentType.objects.all()

        context = {
            'student_source':student_source,
            'student_stage':student_stage,
            'enrollment_type':enrollment_type,
        }
        return render (request,'student/student_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_stage(request):
    if 'create_student' in custom_data_views(request):
        if request.method =="POST":
            student_stage = request.POST['student_stage']
            StudentStage.objects.create(stage=student_stage)
            messages.info(request, "Student Stage Created Successfully.")
            return redirect('student_setup')
        else:
            return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_stage(request,id):
    if 'update_student' in custom_data_views(request):
        if request.method =="POST":
            student_stage = request.POST['student_stage']
            Student = StudentStage.objects.get(id=id)
            Student.stage = student_stage
            Student.save()
            messages.info(request, "Student Stage Updated Successfully.")
            return redirect('student_setup')
        else:
            stage = StudentStage.objects.get(id=id)
            context={
                'stage':stage
            }
            return render(request,'student/edit_stage.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_stage(request,id):
    if 'delete_student' in custom_data_views(request):
        stage_data = StudentStage.objects.get(id=id)
        deleted_role = stage_data.stage
        stage_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_source(request):
    if 'create_student' in custom_data_views(request):
        if request.method =="POST":
            student_source = request.POST['student_source']
            StudentSource.objects.create(source=student_source)
            messages.info(request, "Student Source Created Successfully.")
            return redirect('student_setup')
        else:
            return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_source(request,id):
    if 'update_student' in custom_data_views(request):
        if request.method =="POST":
            student_source = request.POST['student_source']
            Student = StudentSource.objects.get(id=id)
            Student.source = student_source
            Student.save()
            messages.info(request, "Student Source Updated Successfully.")
            return redirect('student_setup')
        else:
            source = StudentSource.objects.get(id=id)
            context={
                'source':source
            }
            return render(request,'student/edit_source.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
      
def delete_source(request,id):
    if 'delete_student' in custom_data_views(request):
        source_data = StudentSource.objects.get(id=id)
        deleted_role = source_data.source
        source_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_enrollment(request):
    if 'create_student' in custom_data_views(request):
        if request.method =="POST":
            enrollment_type = request.POST['enrollment_type']
            EnrollmentType.objects.create( enrollment_type= enrollment_type)
            messages.info(request, "Enrollment Created Successfully.")
            return redirect('student_setup')
        else:
            return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_enrollment(request,id):
    if 'update_student' in custom_data_views(request):
        if request.method =="POST":
            enrollment_type = request.POST['enrollment_type']
            Enrollment = EnrollmentType.objects.get(id=id)
            Enrollment.enrollment_type= enrollment_type
            Enrollment.save()
            messages.info(request, "Enrollment Type Updated Successfully.")
            return redirect('student_setup')
        else:
            enrollment_type = EnrollmentType.objects.get(id=id)
            context={
                'enrollment_type':enrollment_type
            }
            return render(request,'student/edit_enrollment.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_enrollment(request,id):
    if 'delete_student' in custom_data_views(request):
        enrollmentType_data = EnrollmentType.objects.get(id=id)
        deleted_role = enrollmentType_data.enrollment_type
        enrollmentType_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('student_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')        


def student(request):
    if 'read_student' in custom_data_views(request):
        active_student = Student.objects.filter(active=True)
        context = {
            'active_student': active_student,
        }
        return render(request,'student/student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def inactive_student(request):
    if 'read_student' in custom_data_views(request):
        closed_student = Student.objects.filter(active=False)
        context = {
            'closed_student': closed_student
        }
        return render(request,'student/inactive_students.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def my_student(request):
    if 'read_student' in custom_data_views(request):
        try:
            employee = request.user.employee
            my_student = Student.objects.filter(assigned_to=employee)
        except:
            my_student=None
        context = {
            'my_student': my_student
        }
        return render(request,'student/my_student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def add_student(request):
    if 'create_student' in custom_data_views(request):
        if request.method == "POST":
            username = request.POST["username"]
            password=request.POST["password"]
            first_name = request.POST["first_name"]
            last_name=request.POST["last_name"]
            email = request.POST["email"]

            address = request.POST["address"]
            contact = request.POST["contact"]

            enrollment_type = request.POST["enrollment_type"]
            course = request.POST.getlist("course")
            source = request.POST["source"]
            stage = request.POST["stage"]
            assigned_to = request.POST.getlist("assigned_to")
    
            if not username:
                messages.error(request, "The username must be provided.")
                return redirect('add_student')
            try:
                user = User.objects.get(username=username)
                messages.error(request, "Username already exists.")
                return redirect('add_student')

            except User.DoesNotExist:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)

                enrollment_type = EnrollmentType.objects.get(id=enrollment_type)
                source = StudentSource.objects.get(id=source)
                stage = StudentStage.objects.get(id=stage)

                
                user.save()
                student = Student.objects.create(user=user, address=address, contact=contact,enrollment_type=enrollment_type,source=source,stage=stage)
                student.assigned_to.set(assigned_to)
                student.course.set(course)
                student.save()
                messages.info(request, "Student Added Successfully")
                for assign in assigned_to:
                    employee = Employee.objects.get(id=assign)
                    notification_obj = f"You have been assigned a new student: {first_name} {last_name}"
                    notification = EmployeeNotification.objects.create(employee=employee, notification=notification_obj)
                    notification.save()
                return redirect('student')
            
        else:
            enrollment_type = EnrollmentType.objects.all()
            stage = StudentStage.objects.all()
            student_source = StudentSource.objects.all()
            course = Course.objects.all()
            assign = Employee.objects.all()
            context = {
                'enrollment_type':enrollment_type,
                'stage':stage,
                'student_source':student_source,
                'assign':assign,
                'course':course,
            }
            return render(request,'student/add_student.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def edit_student(request,id):
    if 'update_student' in custom_data_views(request):
        if request.method == "POST":
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            log = request.POST.get('log', False)
            if log=="on":
                log=True
            enrollment_type = request.POST["enrollment_type"]
            enrollmenttype = EnrollmentType.objects.get(id=enrollment_type)
            
            source = request.POST["source"]
            student_source = StudentSource.objects.get(id=source)

            

            
            student_data = Student.objects.get(id=id)
            user_data = User.objects.get(username=student_data.user)
            print('usdas')
            user_data.first_name = first_name
            user_data.last_name = last_name
            user_data.email = email
            user_data.username=username
            user_data.save()

            student_data.address = address
            student_data.contact = contact
            student_data.source=student_source
            student_data.log=log
            
            

            student_data.enrollment_type=enrollmenttype
           
          
            student_data.save()

            messages.info(request, "student edited successfully.")
            return redirect('student')
        else:
            student_data = Student.objects.get(id=id)
            enrollment_type = EnrollmentType.objects.all()
            student_source = StudentSource.objects.all()
            course = Course.objects.all()
            

            context = {
                'student_data':student_data,
                'enrollment_type':enrollment_type,
                'student_source':student_source,
                'course':course,
            }
            return render(request,'student/edit_student.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_student(request,id):
    if 'delete_student' in custom_data_views(request):
        delete_student = Student.objects.get(id=id)
        user = User.objects.get(username = delete_student.user)
        deleted_student = delete_student
        delete_student.delete()
        user.delete()
        messages.info(request, f"{deleted_student} Deleted Successfully")
        return redirect('student')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_student(request,id):
    if 'read_student' in custom_data_views(request):
        student = Student.objects.get(id=id)             
        invoices = Invoice.objects.filter(student=id)
        receipts=Receipt.objects.filter(student=id)
        notes=StudentNotes.objects.filter(student=id).order_by('-created')
        logs=StudentLog.objects.filter(student=id).order_by('-created')
        files=StudentFiles.objects.filter(student=id).order_by('-created')
        employee = Employee.objects.all()
        stage=StudentStage.objects.all()
        context = {
            'student': student,
            'invoices':invoices,
            'receipts':receipts,
            'notes':notes,
            'stage':stage,
            'logs':logs,
            'files':files,
            'employee':employee,
        }
        return render(request,'student/view_student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def assign_employee_student(request,id):
    if 'manage_student' in custom_data_views(request):
        if request.method == "POST":
            assigned_user = request.POST.getlist('assigned_user')
            print(assigned_user)
            employees = Employee.objects.filter(id__in=assigned_user)
            student = Student.objects.get(id=id)
            student.assigned_to.set(employees)
            student.save()
            messages.info(request, "Employee assigned successfully")
            

            for assign in assigned_user:
                employee = Employee.objects.get(id=assign)
                notification_obj = f"You have been assigned an existing student: {student.user.first_name} {student.user.last_name}"
                notification = EmployeeNotification.objects.create(employee=employee, notification=notification_obj)
                notification.save()
            
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'Employee Assigned.'
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)

            return redirect('view_student',id)
        else:
            employee = Employee.objects.all()
            print(employee)
            context = {
            'employee':employee,
            }
            return render (request,'inquiry/view_inquiry.html',context)  
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
 
def update_student_stage(request,id):
    if 'update_student' in custom_data_views(request):
        if request.user.is_superuser:
            if request.method =='POST':
                stage = request.POST['stage']
                student_stage = StudentStage.objects.get(id=stage)
                user = User.objects.get(username=request.user)
                changed_by = user.username
                student = Student.objects.get(id=id)
                student.stage = student_stage
                student.save()
                messages.info(request, "student stage updated")
                activity = 'updated student stage to '+str(student_stage)
                StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
                return redirect(view_student,id)
            else:
                return redirect(view_student,id)
        else:
            if request.method =='POST':
                stage = request.POST['stage']
                student_stage = StudentStage.objects.get(id=stage)

                user = User.objects.get(username=request.user)
                changed_by = user.username

                student = Student.objects.filter(id=id)[0]
                student.stage = student_stage
                student.save()
                messages.info(request, "student stage updated")
                activity = 'updated student stage to '+str(student_stage)
                StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
                return redirect(view_student,id)
            else:
                return redirect(view_student,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def add_student_note(request,id):
    if 'create_student' in custom_data_views(request):
        if request.method == 'POST':
            student = Student.objects.get(id=id)
            note_title = request.POST['note_title']
            note = request.POST['note']

            student_notes = StudentNotes.objects.create(student=student, note_title=note_title,note=note)
            student_notes.save()
            messages.info(request, "Student note added successfully")

            activity = 'added note'
            user = User.objects.get(username=request.user)
            changed_by = user.username
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
            return redirect(view_student,id)
        else:
            return redirect('view_student',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




def add_student_file(request,id):
    if 'update_student' in custom_data_views(request):
        if request.user.is_superuser:
            if request.method =='POST':
                title = request.POST['title']
                file = request.FILES['file']
            
                user = User.objects.get(username=request.user)
                added_by = user.username

                student = Student.objects.get(id=id)
                StudentFiles.objects.create(student=student,title=title,file=file,added_by=added_by)
                messages.info(request, "File Added Successfully")

                StudentLog.objects.create(student=student,changed_by=added_by,activity='added file')
                return redirect(view_student,id)
            else:
                return redirect(view_student,id)
        else:
            if request.method =='POST':
                title = request.POST['title']
                file = request.FILES['file']
            
                user = User.objects.get(username=request.user)
                added_by = user.username

                student = student.objects.get(id=id)
                StudentFiles.objects.create(student=student,title=title,file=file,added_by=added_by)
                messages.info(request, "File Added Successfully")

                StudentLog.objects.create(student=student,changed_by=added_by,activity='added file data')
                return redirect(view_student,id)
            else:
                return redirect(view_student,id)

    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def close_student(request,id):
    if 'update_student' in custom_data_views(request):
        if request.user.is_superuser:
            student = Student.objects.get(id=id)
            student.active=False
            student.save()
            messages.info(request, "student closed.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' closed student '
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
            return redirect('view_student',id)
        else:
            student = Student.objects.get(id=id)
            student.active=False
            student.save()
            messages.info(request, "student closed.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' closed student '
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
            return redirect(view_student,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def reopen_student(request,id):
    if 'update_student' in custom_data_views(request):
        if request.user.is_superuser:
            student = Student.objects.get(id=id)
            student.active=True
            student.save()
            messages.info(request, "student reopened.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' reopened student '
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
            return redirect('view_student',id)
        else:
            student = Student.objects.get(id=id)
            student.active=True
            student.save()
            messages.info(request, "student reopened.")

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = ' reopened student '
            StudentLog.objects.create(student=student,changed_by=changed_by,activity=activity)
            return redirect(view_student,id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')






def edit_student_notes(request,id):
    if 'update_student' in custom_data_views(request):
        if request.method == 'POST':
            student = Student.objects.get(id=id)
            notes = request.POST['notes']

            student.notes=notes
            student.save()

            return redirect('')

        else:
            student = Student.objects.get(id=id)
            context = {
                'student': student
            }
            return render(request, '', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    




def change_student_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']

            logged_in_user = request.user

            if logged_in_user.check_password(old_password):
                logged_in_user.password = make_password(new_password)
                logged_in_user.save()
                auth.login(request, logged_in_user)            
                messages.info(request, "Password Changed Successfully.")
                return redirect('student_dashboard')
            else:
                messages.info(request, "Incorrect old password.")
        
        return HttpResponse("Invalid request.")
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('login')
