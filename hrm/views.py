from django.shortcuts import render
from account.context_processors import custom_data_views
# Create your views here.

def hrm(request):
    pass


def add_emp(request):
    if 'create_hrm' in custom_data_views:
        pass