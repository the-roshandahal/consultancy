from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages, auth
from account.models import *
from .models import *

from account.context_processors import custom_data_views
# Create your views here.



def student(request):
    if 'read_finance' in custom_data_views(request):
        student = Student.objects.all()
        context = {
            'student': student
        }
        return render(request,'student/student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def add_student(request):
    if 'create_finance' in custom_data_views(request):
        if request.method == "POST":
            student_name = request.POST["student_name"]
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            Student.objects.create(student_name=student_name,
                                    address=address, email=email, contact=contact)
            return redirect('student')
        else:
            return render(request,'student/add_student.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def edit_student(request,id):
    if 'update_finance' in custom_data_views(request):
        if request.method == "POST":
            student_name = request.POST["student_name"]
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]

            student_data = Student.objects.filter(id=id)[0]

            student_data.student_name = student_name
            student_data.address = address
            student_data.email = email
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
    if 'delete_finance' in custom_data_views(request):
        delete_student = Student.objects.get(id=id)
        deleted_student = delete_student
        delete_student.delete()
        messages.info(request, f"{deleted_student} Deleted Successfully")
        return redirect('student')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def view_student(request,id):
    if 'read_finance' in custom_data_views(request):
        student = Student.objects.get(id=id)
        invoices = Invoice.objects.filter(student=id)[:5]
        receipts = Receipt.objects.filter(student=id)[:5]
        context = {
            'student': student,
            'invoices': invoices,
            'receipts': receipts,
        }
        return render(request,'student/view_student.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')





def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_name = request.POST('file_name')
        student=request.POST['student_id']
        if file:
            student=Student.objects.get(id=student_id)
            Document.objects.create(student=student, file=file, file_name=file_name)
            
            return redirect('document_list')  
    return render(request, 'students/upload_document.html')
    