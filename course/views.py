from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
from account.views import *
from account.models import *
from django.contrib.auth.models import User

from account.context_processors import custom_data_views
# Create your views here.

 
def courses(request):
    if 'read_course' in custom_data_views(request):
        courses = Course.objects.all()
        category = CourseCategory.objects.all()
        context={
            'courses':courses,
            'category':category,
        }
        return render (request,'courses/courses.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def add_course(request):
    if 'create_course' in custom_data_views(request):
        if request.method == "POST":
          
            course_title = request.POST["course_title"]
            course_description = request.POST["course_description"]
            course_price = request.POST["course_price"]
            category = request.POST["course_category"]
            course_category = CourseCategory.objects.get(id=category)
            
            Course.objects.create(course_title=course_title, course_description=course_description, 
                                course_price=course_price, course_category=course_category)
            return redirect('courses')
        else:
            courses = Course.objects.all()
            category = CourseCategory.objects.all()
            context={
                'courses':courses,
                'category':category,
            }
            return render (request,'courses/add_course.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_course(request,id):
    if 'update_course' in custom_data_views(request):
        if request.method == "POST":
            
            course_title = request.POST["course_title"]
            course_description = request.POST["course_description"]
            course_price = request.POST["course_price"]
            

            category = request.POST["course_category"]
            course_category = CourseCategory.objects.get(id=category)
            course_obj = Course.objects.get(id=id)
            course_obj.course_title=course_title
            course_obj.course_description=course_description
            course_obj.course_price=course_price
           
            course_obj.course_category=course_category
            course_obj.save()
            return redirect('courses')
        else:
            course = Course.objects.get(id=id)
            category = CourseCategory.objects.all()
            context={
                'course':course,
                'category':category,
               
            }
            return render (request,'courses/edit_course.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def delete_course(request,id):
    if 'delete_course' in custom_data_views(request):
        course = Course.objects.get(id=id)
        course.delete()
        messages.info(request, "Course Deleted Successfully")
        return redirect('courses')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def course_setup(request):
    if 'read_course' in custom_data_views(request):
        category = CourseCategory.objects.all()
        
        context = {
            'category':category,
           
        }
        return render (request,'courses/course_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
        

def add_course_category(request):
    if 'create_course' in custom_data_views(request):
        if request.method =="POST":
            course_category = request.POST['course_category']
            if CourseCategory.objects.filter(course_category=course_category).exists():
                messages.info(request, "category already exixts")
                return redirect('course_setup')
            else:
                CourseCategory.objects.create(course_category=course_category)
                messages.info(request, "category Added Successfully")
                return redirect('course_setup')

        else:
            return redirect('course_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
        
def edit_course_category(request,id):
    if 'update_course' in custom_data_views(request):
        if request.method =="POST":
            course_category = request.POST['course_category']
            course_category_obj = CourseCategory.objects.get(id=id)
            course_category_obj.course_category=course_category
            course_category_obj.save()
            messages.info(request, "Category updated successfully")
            return redirect('course_setup')
        else:
            course_category = CourseCategory.objects.get(id=id)
            context = {
                'course_category': course_category
                }
            return render(request, 'courses/delete_course.html', context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('course_setup')

        
   

def delete_course_category(request,id):
    if 'delete_course' in custom_data_views(request):
        category = CourseCategory.objects.get(id=id)
        category.delete()
        messages.info(request, "Course Category Deleted Successfully")
        return redirect('course_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')




 
def services(request):
    if 'read_course' in custom_data_views(request):
        services = Service.objects.all()
        category = CourseCategory.objects.all()
        context={
            'services':services,
            'category':category,
        }
        return render (request,'courses/services.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def add_service(request):
    if 'create_course' in custom_data_views(request):
        if request.method == "POST":
          
            service_title = request.POST["service_title"]
            service_description = request.POST["service_description"]
            service_price = request.POST["service_price"]
            category = request.POST["service_category"]
            service_category = CourseCategory.objects.get(id=category)
            
            Service.objects.create(service_title=service_title, service_description=service_description, 
                                service_price=service_price, service_category=service_category)
            return redirect('services')
        else:
            category = CourseCategory.objects.all()
            context={
                'category':category,
            }
            return render (request,'courses/add_service.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_service(request,id):
    if 'update_course' in custom_data_views(request):
        if request.method == "POST":
            
            service_title = request.POST["service_title"]
            service_description = request.POST["service_description"]
            service_price = request.POST["service_price"]
            

            category = request.POST["service_category"]
            service_category = CourseCategory.objects.get(id=category)
            service_obj = Service.objects.get(id=id)
            service_obj.service_title=service_title
            service_obj.service_description=service_description
            service_obj.service_price=service_price
           
            service_obj.service_category=service_category
            service_obj.save()
            return redirect('services')
        else:
            service = Service.objects.get(id=id)
            category = CourseCategory.objects.all()
            context={
                'service':service,
                'category':category,
               
            }
            return render (request,'courses/edit_service.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def delete_service(request,id):
    if 'delete_course' in custom_data_views(request):
        service = Service.objects.get(id=id)
        service.delete()
        messages.info(request, "Course Deleted Successfully")
        return redirect('services')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')