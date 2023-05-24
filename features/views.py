from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View 
from django.urls import reverse


# Create your views here.

def home(request):
    return render(request,'index.html')


# def add_course(request):
# 	if request.method == "POST":
# 		first_name = request.POST['first_name']
# 		last_name = request.POST['last_name']
# 		address=request.POST['address']
# 		email=request.POST['email']
# 		data=Course.objects.create(
# 			first_name=first_name,
# 			last_name=last_name,
# 			address=address,
# 			email=email,
# 			)
# 		data.save()
		
		

# 	else:
# 		return render (request,'student/add_student.html')


# def delete_course(request, course_id):
    
#     course = get_object(Course, id=course_id)
    
#     if request.method == 'POST':
     
#         course.delete()
        
   
#         return redirect('success')
    
  
#     return render(request, 'student/delete_course.html', {'course': course})