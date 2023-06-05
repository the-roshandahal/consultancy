from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("student/", views.student, name="student"),
    path("add_student/", views.add_student, name="add_student"),
    path("edit_student/<int:id>", views.edit_student, name="edit_student"),
    path("delete_student/<int:id>", views.delete_student, name="delete_student"),
    path("view_student/<int:id>", views.view_student, name="view_student"),
    # path("upload_document/", views.upload_document, name="upload_document"),

]