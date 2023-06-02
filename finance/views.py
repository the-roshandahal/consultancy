from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render
from decimal import Decimal
from django.contrib import messages, auth
from django.contrib.auth.models import User
from account.views import *
from account.models import *
from course.models import *
from student.models import *
from .models import *
from account.context_processors import custom_data_views
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Q
from datetime import datetime,date,timedelta

# Create your views here.
def invoice(request):
    if 'read_finance' in custom_data_views(request):
        invoices = Invoice.objects.all()
        context={
            'invoices':invoices
            }
        return render (request, 'finance/invoices.html',context)
    else:
        messages.info(request, "Unauthorized access.")
        return redirect('home')

    


