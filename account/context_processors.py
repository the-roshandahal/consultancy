from hrm.models import *
from django.template.context_processors import request
from features.models import Company
from .models import *

def custom_data(request):
    permissions = []
    company = Company.objects.all().order_by('-created').first()
    if request.user.is_authenticated:
        logged_in_user = User.objects.get(username=request.user)
        # Check if the logged in user is a superuser
        if logged_in_user.is_superuser:
            permissions = ['account', 'finance', 'hrm', 'course', 'leads', 'student',
                           'create_account', 'read_account', 'update_account', 'delete_account', 'manage_account',
                           'create_finance', 'read_finance', 'update_finance', 'delete_finance', 'manage_finance',
                           'create_leads', 'read_leads', 'update_leads', 'delete_leads', 'manage_leads', 
                           'create_hrm', 'read_hrm', 'update_hrm', 'delete_hrm', 'manage_hrm',
                           'create_course', 'read_course', 'update_course', 'delete_course','manage_course',
                           'create_student', 'read_student', 'update_student', 'delete_student', 
                           'manage_company']

            

        else:
            user = Employee.objects.get(user=logged_in_user)
            role=Role.objects.get(role=user.permission)
            permission=Permission.objects.get(role=role)
            

            if permission.create_account or permission.read_account or permission.update_account or permission.delete_account or permission.manage_account:
                permissions.append('account')
            if permission.create_finance or permission.read_finance or permission.update_finance or permission.delete_finance or permission.manage_finance:
                permissions.append('finance')
            if permission.create_hrm or permission.read_hrm or permission.update_hrm or permission.delete_hrm or permission.manage_hrm:
                permissions.append('hrm')
            if permission.create_course or permission.read_course or permission.update_course or permission.delete_course or permission.manage_course:
                permissions.append('course')
            if permission.create_student or permission.read_student or permission.update_student or permission.delete_student or permission.manage_student:
                permissions.append('student')
            if permission.create_leads or permission.read_leads or permission.update_leads or permission.delete_leads or permission.manage_leads:
                permissions.append('leads')


            if permission.create_account:
                permissions.append('create_account')
            if permission.read_account:
                permissions.append('read_account')
            if permission.update_account:
                permissions.append('update_account')
            if permission.delete_account:
                permissions.append('delete_account')
            if permission.manage_account:
                permissions.append('manage_account')


            if permission.create_finance:
                permissions.append('create_finance')
            if permission.read_finance:
                permissions.append('read_finance')
            if permission.update_finance:
                permissions.append('update_finance')
            if permission.delete_finance:
                permissions.append('delete_finance')
            if permission.manage_finance:
                permissions.append('manage_finance')


            if permission.create_hrm:
                permissions.append('create_hrm')
            if permission.read_hrm:
                permissions.append('read_hrm')
            if permission.update_hrm:
                permissions.append('update_hrm')
            if permission.delete_hrm:
                permissions.append('delete_hrm')
            if permission.manage_hrm:
                permissions.append('manage_hrm')


            if permission.create_course:
                permissions.append('create_course')
            if permission.read_course:
                permissions.append('read_course')
            if permission.update_course:
                permissions.append('update_course')
            if permission.delete_course:
                permissions.append('delete_course')
            if permission.manage_course:
                permissions.append('manage_course')

            if permission.create_student:
                permissions.append('create_student')
            if permission.read_student:
                permissions.append('read_student')
            if permission.update_student:
                permissions.append('update_student')
            if permission.delete_student:
                permissions.append('delete_student')
            if permission.manage_student:
                permissions.append('manage_student')


            if permission.create_leads:
                permissions.append('create_leads')
            if permission.read_leads:
                permissions.append('read_leads')
            if permission.update_leads:
                permissions.append('update_leads')
            if permission.delete_leads:
                permissions.append('delete_leads')
            if permission.manage_leads:
                permissions.append('manage_leads')

            if permission.manage_company:
                permissions.append('manage_company')


    return {'permissions': permissions, 'company': company}


def custom_data_views(request):
    
    views_permissions = []
    if request.user.is_authenticated:
        logged_in_user = User.objects.get(username=request.user)
        if logged_in_user.is_superuser:
            views_permissions = ['account', 'finance', 'hrm', 'course', 'leads', 'student',
                           'create_account', 'read_account', 'update_account', 'delete_account', 'manage_account',
                           'create_finance', 'read_finance', 'update_finance', 'delete_finance', 'manage_finance',
                           'create_leads', 'read_leads', 'update_leads', 'delete_leads', 'manage_leads', 
                           'create_hrm', 'read_hrm', 'update_hrm', 'delete_hrm', 'manage_hrm',
                           'create_course', 'read_course', 'update_course', 'delete_course','manage_course',
                           'create_student', 'read_student', 'update_student', 'delete_student', 
                           'manage_company']
            return views_permissions
            

        else:
            
            user = Employee.objects.get(user=logged_in_user)
            role=Role.objects.get(role=user.permission)
            permission=Permission.objects.get(role=role)

            if permission.create_account or permission.read_account or permission.update_account or permission.delete_account or permission.manage_account:
                views_permissions.append('account')
            if permission.create_finance or permission.read_finance or permission.update_finance or permission.delete_finance or permission.manage_finance:
                views_permissions.append('finance')
            if permission.create_hrm or permission.read_hrm or permission.update_hrm or permission.delete_hrm or permission.manage_hrm:
                views_permissions.append('hrm')
            if permission.create_course or permission.read_course or permission.update_course or permission.delete_course or permission.manage_course:
                views_permissions.append('course')
            if permission.create_leads or permission.read_leads or permission.update_leads or permission.delete_leads or permission.manage_leads:
                views_permissions.append('leads')

            if permission.create_account:
                views_permissions.append('create_account')
            if permission.read_account:
                views_permissions.append('read_account')
            if permission.update_account:
                views_permissions.append('update_account')
            if permission.delete_account:
                views_permissions.append('delete_account')
            if permission.manage_account:
                views_permissions.append('manage_account')

            if permission.create_finance:
                views_permissions.append('create_finance')
            if permission.read_finance:
                views_permissions.append('read_finance')
            if permission.update_finance:
                views_permissions.append('update_finance')
            if permission.delete_finance:
                views_permissions.append('delete_finance')
            if permission.manage_finance:
                views_permissions.append('manage_finance')

            if permission.create_hrm:
                views_permissions.append('create_hrm')
            if permission.read_hrm:
                views_permissions.append('read_hrm')
            if permission.update_hrm:
                views_permissions.append('update_hrm')
            if permission.delete_hrm:
                views_permissions.append('delete_hrm')
            if permission.manage_hrm:
                views_permissions.append('manage_hrm')

            if permission.create_course:
                views_permissions.append('create_course')
            if permission.read_course:
                views_permissions.append('read_course')
            if permission.update_course:
                views_permissions.append('update_course')
            if permission.delete_course:
                views_permissions.append('delete_course')
            if permission.manage_course:
                views_permissions.append('manage_course')
            
            if permission.create_student:
                views_permissions.append('create_student')
            if permission.read_student:
                views_permissions.append('read_student')
            if permission.update_student:
                views_permissions.append('update_student')
            if permission.delete_student:
                views_permissions.append('delete_student')
            if permission.manage_student:
                views_permissions.append('manage_student')
            

            if permission.create_leads:
                views_permissions.append('create_leads')
            if permission.read_leads:
                views_permissions.append('read_leads')
            if permission.update_leads:
                views_permissions.append('update_leads')
            if permission.delete_leads:
                views_permissions.append('delete_leads')
            if permission.manage_leads:
                views_permissions.append('manage_leads')
                
            if permission.manage_company:
                views_permissions.append('manage_company')
            
            return views_permissions
    else:
        return views_permissions
