from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from account.models import *
from account.context_processors import *

# def homepage(request):
#     if request.user.is_authenticated:
#         return redirect('home') 
#     else:
#         return render (request,'homepage.html')

def home(request):
    if request.user.is_authenticated:
        return render (request,'index.html') 
    else:
        return redirect('login')
    





def company_setup(request):
    if 'manage_company' in custom_data_views(request):
        company_setup= Company.objects.all().order_by('-created').first()
        context = {
            'company_setup':company_setup,
        }
        return render (request,'features/company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    




def add_company_setup(request):
    if 'manage_company' in custom_data_views(request):
        if Company.objects.all().exists():
            messages.info(request, "You have already added a setup.")
            return redirect('company_setup')
        else:
            if request.method=='POST':
                company_name = request.POST['company_name']
                company_address = request.POST['company_address']
                company_email = request.POST['company_email']
                company_contact_number = request.POST['company_contact_number']
                company_logo = request.FILES['company_logo']
                payment_terms = request.POST['payment_terms']

                Company.objects.create(company_name = company_name,company_address = company_address,
                                    company_email = company_email,company_contact_number = company_contact_number,company_logo = company_logo,
                                    payment_terms = payment_terms)
                return redirect('company_setup')
            else:
                return render(request,'features/add_company_setup.html')
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
    


def edit_company_setup(request,id):
    if 'manage_company' in custom_data_views(request):
        if request.method=='POST':
            setup = Company.objects.get(id=id)
            setup.company_name = request.POST['company_name']
            setup.company_address = request.POST['company_address']
            setup.company_email = request.POST['company_email']
            setup.company_contact_number = request.POST['company_contact_number']
            setup.payment_terms = request.POST['payment_terms']
            setup.payment_details = request.POST['payment_details']

            if request.FILES and request.FILES['company_logo']:
                setup.company_logo = request.FILES['company_logo']
            setup.save()
            return redirect('company_setup')
        else:
            setup = Company.objects.get(id=id)
            print(setup.company_name)
            context = {
            'setup':setup
            }
            return render(request,'features/edit_company_setup.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')
  


