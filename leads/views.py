from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
# import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *

from account.context_processors import custom_data_views
# Create your views here.

def crm_setup(request):
    if 'read_leads' in custom_data_views(request):
        lead_stage = LeadStage.objects.all()
        lead_source = LeadSource.objects.all()
        context = {
            'lead_source':lead_source,
            'lead_stage':lead_stage,
        }
        return render (request,'leads/crm_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_stage(request):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_stage = request.POST['lead_stage']
            LeadStage.objects.create(stage=lead_stage)
            messages.info(request, "Lead Stage Created Successfully.")
            return redirect('crm_setup')
        else:
            return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_stage(request,id):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_stage = request.POST['lead_stage']
            lead = LeadStage.objects.get(id=id)
            lead.stage = lead_stage
            lead.save()
            messages.info(request, "Lead Stage Updated Successfully.")
            return redirect('crm_setup')
        else:
            stage = LeadStage.objects.get(id=id)
            context={
                'stage':stage
            }
            return render(request,'leads/edit_stage.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    
def delete_stage(request,id):
    if 'delete_leads' in custom_data_views(request):
        stage_data = LeadStage.objects.get(id=id)
        deleted_role = stage_data.stage
        stage_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def create_source(request):
    if 'create_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_source = request.POST['lead_source']
            LeadSource.objects.create(source=lead_source)
            messages.info(request, "Lead Source Created Successfully.")
            return redirect('crm_setup')
        else:
            return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

def edit_source(request,id):
    if 'manage_leads' in custom_data_views(request):
        if request.method =="POST":
            lead_source = request.POST['lead_source']
            lead = LeadSource.objects.get(id=id)
            lead.source = lead_source
            lead.save()
            messages.info(request, "Lead Source Updated Successfully.")
            return redirect('crm_setup')
        else:
            source = LeadSource.objects.get(id=id)
            context={
                'source':source
            }
            return render(request,'leads/edit_source.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
      
def delete_source(request,id):
    if 'delete_leads' in custom_data_views(request):
        source_data = LeadSource.objects.get(id=id)
        deleted_role = source_data.source
        source_data.delete()
        messages.info(request, f"{deleted_role} Deleted Successfully")
        return redirect('crm_setup')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')


