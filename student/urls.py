from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [

    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),

    path("student/", views.student, name="student"),
    path("student_setup/", views.student_setup, name="student_setup"),
    path("create_stage/", views.create_stage, name="create_stage"),
    path("edit_stage/<int:id>", views.edit_stage, name="edit_stage"),
    path("create_source/", views.create_source, name="create_source"),
    path("edit_source/<int:id>", views.edit_source, name="edit_source"),
    path("create_enrollment/", views.create_enrollment, name="create_enrollment"),
    path("edit_enrollment/<int:id>", views.edit_enrollment, name="edit_enrollment"),
    path("delete_stage/<int:id>", views.delete_stage, name="delete_stage"),
    path("delete_source/<int:id>", views.delete_source, name="delete_source"),
    path("delete_enrollment/<int:id>", views.delete_enrollment, name="delete_enrollment"),
  
  

    path("add_student/", views.add_student, name="add_student"),
    path("edit_student/<int:id>", views.edit_student, name="edit_student"),
    path("delete_student/<int:id>", views.delete_student, name="delete_student"),
    path("view_student/<int:id>", views.view_student, name="view_student"),


    path("update_student_stage/<int:id>", views.update_student_stage, name="update_student_stage"),
    path("add_student_note/<int:id>", views.add_student_note, name="add_student_note"),
    path("add_student_file/<int:id>", views.add_student_file, name="add_student_file"),
    path("close_student/<int:id>", views.close_student, name="close_student"),
    # path("update_users/<int:id>", views.update_users, name="update_users"),
    path("reopen_student/<int:id>", views.reopen_student, name="reopen_student"),
]