from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import *
from hrm.models import *
from account.models import*
from account.context_processors import custom_data_views
import logging
# Create your views here.
def inquiry(request):
    if 'read_inquiry' in custom_data_views(request):
        new_inquiries = StudentInquiry.objects.filter(is_active = True, is_verified = False).order_by('created')
        context={
            'new_inquiries':new_inquiries,
        }
        return render(request,'inquiry/inquiry.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

    
def active_inquiries(request):
    if 'read_inquiry' in custom_data_views(request):
        active_inquiries = StudentInquiry.objects.filter(is_active = True, is_verified= True).order_by('-created')
        context={
                'active_inquiries':active_inquiries,
        }
        return render(request,'inquiry/active_inquiries.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def my_inquiries(request):
    if 'read_inquiry' in custom_data_views(request):
        logged_in_user = User.objects.get(username=request.user)
        print(logged_in_user)
        try:
            employee = Employee.objects.get(user=logged_in_user)
            my_inquiries = StudentInquiry.objects.filter(is_active = True, is_verified= True,assigned=employee).order_by('-created')
            my_inactive_inquiries = StudentInquiry.objects.filter(is_active = False, is_verified= True,assigned=employee).order_by('-created')
        except:
            my_inquiries= None
            my_inactive_inquiries= None

        context={
            'my_inquiries':my_inquiries,
            'my_inactive_inquiries':my_inactive_inquiries,
        }
        return render(request,'inquiry/my_inquiries.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def inactive_inquiry(request):
    if 'read_inquiry' in custom_data_views(request):
        inactive_inquiries = StudentInquiry.objects.filter(is_active = False)
        context={
            'inactive_inquiries':inactive_inquiries
        }
        return render(request,'inquiry/inactive_inquiries.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def view_inquiry(request,id):
    if 'read_inquiry' in custom_data_views(request):
        inquiry_data = StudentInquiry.objects.get(id=id)
        logs = InquiryLogs.objects.filter(inquiry=id).order_by('-created')
        notes = InquiryNote.objects.filter(inquiry=id)
        stage = InquiryStage.objects.all()
        context={
            'inquiry_data':inquiry_data,
            'logs':logs,
            'notes':notes,
            'stage':stage,
        }
        return render(request,'inquiry/view_inquiry.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def add_inquiry(request):
    if 'create_inquiry' in custom_data_views(request):
        if request.method == "POST":
            first_name = request.POST["first_name"]
            last_name=request.POST["last_name"]
            dob=request.POST["dob"]
            email = request.POST["email"]
            guardian_name = request.POST["guardian_name"]
            marital_status = request.POST["marital_status"]
            contact = request.POST["contact"]
            temporary_address = request.POST["temporary_address"]
            permanent_address = request.POST["permanent_address"]
            date=request.POST["consultation_date"]
            remarks=request.POST["remarks"]
            
            purpose=request.POST["purpose"]
            purpose= InquiryPurpose.objects.get(id=purpose)
            
            
            institution1 = request.POST["institution1"]
            passed_year1 = request.POST["passed_year1"]
            percentage1 = request.POST["percentage1"]

            institution2 = request.POST["institution2"]
            passed_year2 = request.POST["passed_year2"]
            percentage2 = request.POST["percentage2"]

            institution3 = request.POST["institution3"]
            passed_year3 = request.POST["passed_year3"]
            percentage3 = request.POST["percentage3"]

            other = request.POST["other"]

            course = request.POST["course"]
            college = request.POST["college"]
            country = request.POST["country"]
            city =request.POST["city"]
            intake = request.POST["intake"]
            applied_country = request.POST["country"]
            applied_date = request.POST["date"]
          

            assigned_user = request.POST['assigned_user']
            assigned = Employee.objects.get(id=assigned_user)
            
            inquiry = StudentInquiry.objects.create(first_name=first_name,last_name=last_name, dob=dob, temporary_address=temporary_address,permanent_address=permanent_address,contact=contact,email=email,guardian_name=guardian_name,marital_status=marital_status,purpose=purpose,date=date,remarks=remarks,course=course,college=college,country=country,city=city,intake=intake,applied_date=applied_date,applied_country=applied_country,assigned=assigned,
                                             other=other, institution1=institution1, passed_year1=passed_year1,percentage1=percentage1, institution2=institution2, passed_year2=passed_year2,percentage2=percentage2, institution3=institution3, passed_year3=passed_year3,percentage3=percentage3)
            
            inquiry.save()
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'created inquiry'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('inquiry')
          
            
        else:
            inquiry=StudentInquiry.objects.all()
            user = Employee.objects.all()
            purpose=InquiryPurpose.objects.all()
            context = {
                'inquiry':inquiry,
                'user':user,
                'purpose':purpose,
        
            }
            return render(request,'inquiry/add_inquiry.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_inquiry(request,id):
    from account.context_processors import custom_data_views
    if 'update_inquiry' in custom_data_views(request):
        if request.method == "POST":
            first_name = request.POST["first_name"]
            last_name=request.POST["last_name"]
            dob=request.POST["dob"]
            email = request.POST["email"]
            guardian_name = request.POST["guardian_name"]
            marital_status = request.POST["marital_status"]
            contact = request.POST["contact"]
            temporary_address = request.POST["temporary_address"]
            permanent_address = request.POST["permanent_address"]
            date=request.POST["consultation_date"]
            remarks=request.POST["remarks"]
            
            purpose=request.POST["purpose"]
            purposes= InquiryPurpose.objects.get(id=purpose)
            
            
            institution1 = request.POST["institution1"]
            passed_year1 = request.POST["passed_year1"]
            percentage1 = request.POST["percentage1"]

            institution2 = request.POST["institution2"]
            passed_year2 = request.POST["passed_year2"]
            percentage2 = request.POST["percentage2"]

            institution3 = request.POST["institution3"]
            passed_year3 = request.POST["passed_year3"]
            percentage3 = request.POST["percentage3"]


            other = request.POST["other"]
             
            course = request.POST["course"]
            college = request.POST["college"]
            country = request.POST["country"]
            city =request.POST["city"]
            intake = request.POST["intake"]
            applied_country = request.POST["country"]
            applied_date = request.POST["date"]
          
     
            inquiry = StudentInquiry.objects.get(id=id)

            inquiry.first_name=first_name
            inquiry.last_name=last_name
            inquiry.email=email
            inquiry.contact=contact
            inquiry.temporary_address=temporary_address
            inquiry.permanent_address=permanent_address
            inquiry.purpose=purposes
            inquiry.dob=dob
            inquiry.guardian_name=guardian_name
            inquiry.marital_status=marital_status
            inquiry.remarks=remarks
            inquiry.date=date
            
            inquiry.institution1 = institution1
            inquiry.passed_year1 = passed_year1
            inquiry.percentage1 = percentage1

            inquiry.institution2 = institution2
            inquiry.passed_year2 = passed_year2
            inquiry.percentage2 = percentage2

            inquiry.institution3 = institution3
            inquiry.passed_year3 = passed_year3
            inquiry.percentage3 = percentage3

            inquiry.course = course
            inquiry. college = college
            inquiry.country = country
            inquiry.city = city
            inquiry.intake = intake
            inquiry.applied_country = applied_country
            inquiry.applied_date = applied_date 
            inquiry.other=other
            inquiry.save()

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'edited inquiry'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('view_inquiry',id)
        
        else:
           inquiry = StudentInquiry.objects.get(id=id)
           user = Employee.objects.all()
           purpose = InquiryPurpose.objects.all()
           context = {
                'inquiry':inquiry,
                'purpose':purpose,
                'user':user,
            }
        return render (request,'inquiry/edit_inquiry.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    

def add_inquiry_note(request,id):
    if 'create_inquiry' in custom_data_views(request):
        if request.method == "POST":
            note_title = request.POST['note_title']
            note = request.POST['note']
            inquiry = StudentInquiry.objects.get(id=id)
            InquiryNote.objects.create(inquiry=inquiry,note=note,note_title=note_title)

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'added note'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('view_inquiry',id)
        else:
            return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def add_consultation_date(request,id):
    if 'create_inquiry' in custom_data_views(request):
        if request.method == "POST":
            consultation_date = request.POST['consultation_date']
            inquiry = StudentInquiry.objects.get(id=id)
            inquiry.consultation_date=consultation_date
            inquiry.save()
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'Updated consultation date'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)

            return redirect('view_inquiry',id)
        else:
            return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def assign_employee(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method == "POST":
            assigned_user = request.POST['assigned_user']
            assigned = Employee.objects.get(id=assigned_user)
            inquiry = StudentInquiry.objects.get(id=id)
            inquiry.assigned=assigned
            inquiry.save()
            
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'Employee Assigned.'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)

            return redirect('view_inquiry',id)
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
    

def update_inquiry_stage(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method == "POST":
            stage = request.POST['stage']
            inquiry = StudentInquiry.objects.get(id=id)
            inquiry.stage=stage
            inquiry.save()

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'updated stage to '+ str(stage)
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)

            return redirect('view_inquiry',id)
        else:
            return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def delete_inquiry(request,id):
    if 'delete_inquiry' in custom_data_views(request):
        inquiry = StudentInquiry.objects.get(id=id)
        inquiry.delete()
        return redirect('inquiry')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def verify_inquiry(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method =="POST":
            inquiry = StudentInquiry.objects.get(id=id)
            inquiry.is_verified=True
            inquiry.save()
            messages.info(request, "inquiry verified.")
    
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'inquiry is verified'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')  
         
def close_inquiry(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method =="POST":
            closed_reason = request.POST['closed_reason']
            inquiry = StudentInquiry.objects.get(id=id)
            inquiry.is_active=False
            inquiry.closed_reason=closed_reason
            inquiry.save()
            messages.info(request,"inquiry closed.")
    
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'closed inquiry '
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')    

def reopen_inquiry(request,id):
    if 'manage_inquiry' in custom_data_views(request):
      
        inquiry = StudentInquiry.objects.get(id=id)
        inquiry.is_active=True
        inquiry.closed_reason=None
        inquiry.save()
        messages.info(request, "inquiry reopend.")

        user = User.objects.get(username=request.user)
        changed_by = user.username
        activity = 'reopend inquiry '
        InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
        return redirect('view_inquiry',id)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


def inquiry_setup(request):
    if 'manage_inquiry' in custom_data_views(request):
        stage=InquiryStage.objects.all()
        purpose=InquiryPurpose.objects.all()
        context = {
            'stage':stage,
            'purpose':purpose,
        }
        return render(request,'inquiry/inquiry_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def create_stages(request):
    if 'create_inquiry' in custom_data_views(request):
        if request.method =="POST":
            stage = request.POST['stage']
            InquiryStage.objects.create(stage=stage)
            messages.info(request, "Stage Created Successfully.")
            return redirect('inquiry_setup')
        else:
            return redirect('inquiry_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def edit_stages(request,id):
    if 'update_inquiry' in custom_data_views(request):
        if request.method =="POST":
            inquiry_stage = request.POST['stage']
            Inquiry=InquiryStage.objects.get(id=id)   
            Inquiry.stage=inquiry_stage  
            Inquiry.save()  
            messages.info(request, "Stage Edited Successfully.")
            return redirect('inquiry_setup')
        else:
            stage=InquiryStage.objects.get(id=id)
            context = {
                'stage':stage,
            }
            return render(request, 'inquiry/edit_stage.html',context )
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_stages(request,id):
    if 'delete_inquiry' in custom_data_views(request):
        stage = InquiryStage.objects.get(id=id)
        deleted_role = stage.stage
        stage.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('inquiry_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')    

def create_purpose(request):
    if 'create_inquiry' in custom_data_views(request):
        if request.method =="POST":
            purpose = request.POST['purpose']
            InquiryPurpose.objects.create(purpose=purpose)
            messages.info(request, "Purpose Created Successfully.")
            return redirect('inquiry_setup')
        else:
            return redirect('inquiry_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')    
    
def edit_purpose(request,id):
    if 'update_inquiry' in custom_data_views(request):
        if request.method =="POST":
            inquiry_purpose= request.POST['purpose']
            Inquiry=InquiryPurpose.objects.get(id=id)   
            Inquiry.purpose=inquiry_purpose
            Inquiry.save()  
            messages.info(request, "Stage Edited Successfully.")
            return redirect('inquiry_setup')
        else:
            purpose=InquiryPurpose.objects.get(id=id)
            context = {
                'purpose':purpose,
            }
            return render(request, 'inquiry/edit_purpose.html',context )
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def delete_purpose(request,id):
    if 'delete_inquiry' in custom_data_views(request):
        purpose = InquiryPurpose.objects.get(id=id)
        deleted_role = purpose.purpose
        purpose.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('inquiry_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def external_inquiry(request):
    if request.method =="POST":
        first_name = request.POST["first_name"]
        last_name=request.POST["last_name"]
        dob=request.POST["dob"]
        email = request.POST["email"]
        guardian_name = request.POST["guardian_name"]
        marital_status = request.POST["marital_status"]
        contact = request.POST["contact"]
        temporary_address = request.POST["temporary_address"]
        permanent_address = request.POST["permanent_address"]
        date=request.POST["consultation_date"]
        remarks=request.POST["remarks"]
        
        purpose=request.POST["purpose"]
        purpose= InquiryPurpose.objects.get(id=purpose)
        
        
        institution1 = request.POST["institution1"]
        passed_year1 = request.POST["passed_year1"]
        percentage1 = request.POST["percentage1"]

        institution2 = request.POST["institution2"]
        passed_year2 = request.POST["passed_year2"]
        percentage2 = request.POST["percentage2"]

        institution3 = request.POST["institution3"]
        passed_year3 = request.POST["passed_year3"]
        percentage3 = request.POST["percentage3"]

        other = request.POST["other"]

        course = request.POST["course"]
        college = request.POST["college"]
        country = request.POST["country"]
        city =request.POST["city"]
        intake = request.POST["intake"]
        applied_country = request.POST["country"]
        applied_date = request.POST["date"]
        

        
        inquiry = StudentInquiry.objects.create(first_name=first_name,last_name=last_name, dob=dob, temporary_address=temporary_address,permanent_address=permanent_address,contact=contact,email=email,guardian_name=guardian_name,marital_status=marital_status,purpose=purpose,date=date,remarks=remarks,course=course,college=college,country=country,city=city,intake=intake,applied_date=applied_date,applied_country=applied_country,
                                            other=other, institution1=institution1, passed_year1=passed_year1,percentage1=percentage1, institution2=institution2, passed_year2=passed_year2,percentage2=percentage2, institution3=institution3, passed_year3=passed_year3,percentage3=percentage3)
        
        inquiry.save()
        user = User.objects.get(username=request.user)
        changed_by = user.username
        activity = 'created inquiry'
        InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
        return redirect('inquiry')
    else:
        purpose = InquiryPurpose.objects.all()
        context = {
            'purpose':purpose
        }
        return render(request,'inquiry/external_inquiry.html',context)