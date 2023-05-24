from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View 
from django.urls import reverse


# Create your views here.


def add_student(request):
	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		address=request.POST['address']
		email=request.POST['email']
        contact = request.POST["contact"]
		data=Student.objects.create(
			first_name=first_name,
			last_name=last_name,
			address=address,
			email=email,
			)
		data.save()
		
		

	else:
		return render (request,'student/add_student.html')

def add_student(request):
    if request.method == "POST":
            name = request.POST["name"]
            last_name = request.POST['last_name']
            address = request.POST["address"]
            email = request.POST["email"]
            contact = request.POST["contact"]
            Student.objects.create(name=name,last_name=name,
                                    address=address, email=email, contact=contact)
            return redirect('student')
        else:
            return render(request,'student/add_student.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
        
           

            
def delete_student(request, _id):
    
    
    