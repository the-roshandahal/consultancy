from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def inquiry(request):
    active_inquiries = Inquiry.objects.filter(is_active = True)
    context={
        'active_inquiries':active_inquiries,
    }
    return render(request,'inquiry/inquiry.html',context)

def inactive_inquiry(request):
    inactive_inquiries = Inquiry.objects.filter(is_active = False)
    context={
        'inactive_inquiries':inactive_inquiries
    }
    return render(request,'inquiry/inactive_inquiries.html',context)

def view_inquiry(request,id):
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


def add_inquiry(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        purpose = request.POST['purpose']
        education_qualification = request.POST['education_qualification']
        description = request.POST.get('description', '')
        consultation_date = request.POST.get('consultation_date', '')
        stage = "initial"
        source = "reception-inquiry"
        inquiry = Inquiry.objects.create(first_name =first_name, last_name =last_name, email =email, contact=contact,
                                         address =address, purpose =purpose, stage =stage, education_qualification=education_qualification,
                                         description =description, consultation_date =consultation_date,source=source)
        inquiry.save()
        user = User.objects.get(username=request.user)
        changed_by = user.username
        activity = 'created inquiry'
        InquiryLogs.objects.create(inquiry=inquiry,changed_by=changed_by,activity=activity)
        return redirect('inquiry')
        
    else:
        stage = InquiryStage.objects.all()
        purpose = Purpose.objects.all()
        context = {
            'stage':stage,
            'purpose':purpose,
        }
        return render (request,'inquiry/add_inquiry.html',context)
    

def add_inquiry_note(request,id):
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
    
    

def update_inquiry_stage(request,id):
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
    