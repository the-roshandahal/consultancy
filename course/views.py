from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
from account.views import *
from account.models import *
from django.contrib.auth.models import User

from account.context_processors import custom_data_views
# Create your views here.

 
def courses(request):
    if 'read_product' in custom_data_views(request):
        coursess = Course.objects.all()
        category = CourseCategory.objects.all()
        unit = CourseUnit.objects.all()
        context={
            'courses':courses,
            'category':category,
            'unit':unit,
        }
        return render (request,'courses/courses.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def add_course(request):
    if 'create_courses' in custom_data_views(request):
        if request.method == "POST":
            course_type = request.POST["course_type"]
            course_title = request.POST["course_title"]
            course_description = request.POST["course_description"]
            course_price = request.POST["course_price"]
            
            

            category = request.POST["course_category"]
            unit = request.POST["course_unit"]
            course_category = CourseCategory.objects.get(id=category)
            course_unit = CourseUnit.objects.get(id=unit)
            
            Course.objects.create(course_type=course_type,course_title=course_title, course_description=course_description, 
                                course_price=course_price, course_category=course_category,course_unit=course_unit)
            return redirect(courses)
        else:
            courses = Course.objects.all()
            category = CourseCategory.objects.all()
            unit = CourseUnit.objects.all()
            context={
                'courses':courses,
                'category':category,
                'unit':unit,
            }
            return render (request,'courses/add_course.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def edit_course(request,id):
    if 'update_courses' in custom_data_views(request):
        if request.method == "POST":
            course_type = request.POST["course_type"]
            course_title = request.POST["course_title"]
            course_description = request.POST["course_description"]
            course_price = request.POST["course_price"]
            

            category = request.POST["course_category"]
            unit = request.POST["course_unit"]
            course_category = CourseCategory.objects.get(id=category)
            course_unit = CourseUnit.objects.get(id=unit)
            course_obj = Course.objects.get(id=id)
            course_obj.course_type=course_type
            course_obj.course_title=course_title
            course_obj.course_description=course_description
            course_obj.course_price=course_price
           
            course_obj.course_category=course_category
            course_obj.course_unit=course_unit
            course_obj.save()
            return redirect(courses)
        else:
            course = Course.objects.get(id=id)
            category = CourseCategory.objects.all()
            unit = CourseUnit.objects.all()
            context={
                'course':course,
                'category':category,
                'unit':unit,
            }
            return render (request,'courses/edit_course.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def delete_course(request,id):
    if 'delete_courses' in custom_data_views(request):
        course = Course.objects.get(id=id)
        course.delete()
        messages.info(request, "Course Deleted Successfully")
        return redirect(courses)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

    

def add_course_category(request):
    if 'create_courses' in custom_data_views(request):
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
        messages.info(request, "Unauthorized access.")
        return redirect('home')
        
def edit_course_category(request,id):
    if 'update_courses' in custom_data_views(request):
        return render (request,'courses/delete_course.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def delete_course_category(request,id):
    if 'delete_courses' in custom_data_views(request):
        category = CourseCategory.objects.get(id=id)
        category.delete()
        messages.info(request, "Course Category Deleted Successfully")
        return redirect('course_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

