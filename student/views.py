from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages, auth
from account.models import *

from account.context_processors import custom_data_views
# Create your views here.



def student(request):
    if 'read_student' in custom_data_views(request):
        student = Student.objects.all()
        context = {
            'student': student
        }
        return render(request,'student/student.html', context)
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
            log = request.POST["log"]
            
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

                if log == "on":
                    log_status = True
                else:
                    log_status= False

                user.save()
                student = Student.objects.create(user=user, address=address, contact=contact,enrollment_type=enrollment_type,source=source,stage=stage,log_status = log_status)
                student.assigned_to.set(assigned_to)
                student.course.set(course)
                student.save()
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
            student_data.save()

            messages.info(request, "student edited successfully.")
            return redirect('student')
        else:
            student_data = Student.objects.filter(id=id)[0]
            context = {
                'student_data':student_data
            }
            return render(request,'student/edit_student.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_student(request,id):
    print('hello')
    if 'delete_student' in custom_data_views(request):
        delete_student = Student.objects.get(id=id)
        deleted_student = delete_student
        delete_student.delete()
        messages.info(request, f"{deleted_student} Deleted Successfully")
        return redirect('student')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_student(request,id):
    if 'read_student' in custom_data_views(request):
        student = Student.objects.get(id=id)
        # invoices = Invoice.objects.filter(student=id)[:5]
        # receipts = Receipt.objects.filter(student=id)[:5]
        context = {
            'student': student,
        }
        return render(request,'student/view_student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')





# def upload_document(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         file_name = request.POST('file_name')
#         student=request.POST['student_id']
#         if file:
#             student=Student.objects.get(id=student)
#             Document.objects.create(student=student, file=file, file_name=file_name)
            
#             return redirect('document_list')  
#     return render(request, 'students/upload_document.html')
    