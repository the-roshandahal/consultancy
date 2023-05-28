from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("courses/", views.courses, name="courses"),
    path("add_course/", views.add_course, name="add_course"),
    path("edit_course/<int:id>", views.edit_course, name="edit_course"),
    path("delete_course/<int:id>", views.delete_course, name="delete_course"),

    path("course_setup/", views.course_setup, name="course_setup"),

    path("add_course_category/", views.add_course_category, name="add_course_category"),
    path("edit_course_category/<int:id>", views.edit_course_category, name="edit_course_category"),
    path("delete_course_category/<int:id>", views.delete_course_category, name="delete_course_category"),


]