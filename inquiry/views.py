from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import *
from hrm.models import *
from account.context_processors import custom_data_views
# Create your views here.
def inquiry(request):
    if 'read_inquiry' in custom_data_views(request):
        new_inquiries = Inquiry.objects.filter(is_active = True, is_verified = False).order_by('created')
        context={
            'new_inquiries':new_inquiries,
        }
        return render(request,'inquiry/inquiry.html',context)
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
            purpose = request.POST["purpose"]
            date=request.POST["consultation_date"]
            remarks=request.POST["remarks"]
            
            
            institution = request.POST["instution1"]
            passed_year = request.POST["passed_year1"]
            percentage = request.POST["percentage1"]
            other = request.POST["other"]

              
            course = request.POST["course"]
            college = request.POST["college"]
            country = request.POST["country"]
            city =request.POST["city"]
            intake = request.POST["intake"]
            applied_before = request.POST["applied_before"]
            applied_country = request.POST["country"]
            applied_date = request.POST["date"]
          

            assigned_user = request.POST['assigned_user']
            assigned = Employee.objects.get(id=assigned_user)
            
            inquiry = Inquiry.objects.create(first_name=first_name,last_name=last_name, dob=dob, temporary_address=temporary_address,permanent_address=permanent_address,contact=contact,email=email,guardian_name=guardian_name,marital_status=marital_status,purpose=purpose,date=date,remarks=remarks,course=course,college=college,country=country,city=city,intake=intake,applied_before=applied_before,applied_date=applied_date,applied_country=applied_country,assigned=assigned,
                                             other=other, institution=institution, passed_year=passed_year,percentage=percentage,is_taken=is_taken)
            
            inquiry.save()
            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'created inquiry'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('inquiry')
          
            
        else:
            inquiry=Inquiry.objects.all()
            user = Employee.objects.all()
            context = {
                'inquiry':inquiry,
                'user':user,
        
            }
            return render(request,'inquiry/add_inquiry.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def active_inquiries(request):
    if 'read_inquiry' in custom_data_views(request):
        active_inquiries = Inquiry.objects.filter(is_active = True, is_verified= True).order_by('-created')
        context={
                'active_inquiries':active_inquiries,
        }
        return render(request,'inquiry/my_inquiries.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')



def my_inquiries(request):
    if 'read_inquiry' in custom_data_views(request):
        logged_in_user = User.objects.get(username=request.user)
        print(logged_in_user)
        try:
            employee = Employee.objects.get(user=logged_in_user)
            my_inquiries = Inquiry.objects.filter(is_active = True, is_verified= True,assigned=employee).order_by('-created')
            my_inactive_inquiries = Inquiry.objects.filter(is_active = False, is_verified= True,assigned=employee).order_by('-created')
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
        inactive_inquiries = Inquiry.objects.filter(is_active = False)
        context={
            'inactive_inquiries':inactive_inquiries
        }
        return render(request,'inquiry/inactive_inquiries.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def view_inquiry(request,id):
    if 'read_inquiry' in custom_data_views(request):
        inquiry_data = Inquiry.objects.get(id=id)
        logs = InquiryLogs.objects.filter(inquiry=id).order_by('-created')
        notes = InquiryNotes.objects.filter(inquiry=id)
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


def edit_inquiry(request,id):
    from account.context_processors import custom_data_views
    if 'update_inquiry' in custom_data_views(request):
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            purpose = request.POST['purpose']
            education_qualification = request.POST['education_qualification']
            description = request.POST.get('description', '')

            inquiry = Inquiry.objects.get(id=id)

            inquiry.first_name=first_name
            inquiry.last_name=last_name
            inquiry.email=email
            inquiry.contact=contact
            inquiry.address=address
            inquiry.purpose=purpose
            inquiry.education_qualification=education_qualification
            inquiry.description=description
            inquiry.save()

            user = User.objects.get(username=request.user)
            changed_by = user.username
            activity = 'edited inquiry'
            InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
            return redirect('view_inquiry',id)
        
        else:
           inquiry = Inquiry.objects.get(id=id)
           purpose = Purpose.objects.all()
           context = {
                'inquiry':inquiry,
                'purpose':purpose,
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
            inquiry = Inquiry.objects.get(id=id)
            InquiryNotes.objects.create(inquiry=inquiry,note=note,note_title=note_title)

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
            inquiry = Inquiry.objects.get(id=id)
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
    

def update_inquiry_stage(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method == "POST":
            stage = request.POST['stage']
            inquiry = Inquiry.objects.get(id=id)
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
        inquiry = Inquiry.objects.get(id=id)
        inquiry.delete()
        return redirect('inquiry')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def close_inquiry(request,id):
    if 'manage_inquiry' in custom_data_views(request):
        if request.method =="POST":
            closed_reason = request.POST['closed_reason']
            inquiry = Inquiry.objects.get(id=id)
            inquiry.is_active=False
            inquiry.closed_reason=closed_reason
            inquiry.save()
            messages.info(request, "inquiry closed.")
    
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
        print("reopen")
        inquiry = Inquiry.objects.get(id=id)
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
        return render(request,'inquiry/inquiry_setup.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    



def external_inquiry(request):
    purpose = Purpose.objects.all()
    context = {
        'purpose':purpose
    }
    return render(request,'inquiry/external_inquiry.html',context)