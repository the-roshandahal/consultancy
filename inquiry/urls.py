from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [

    path("inquiry/", views.inquiry, name="inquiry"),
    path("inactive_inquiry/", views.inactive_inquiry, name="inactive_inquiry"),
    path("add_inquiry/", views.add_inquiry, name="add_inquiry"),
    path("view_inquiry/<int:id>", views.view_inquiry, name="view_inquiry"),
    path("add_inquiry_note/<int:id>", views.add_inquiry_note, name="add_inquiry_note"),
    path("update_inquiry_stage/<int:id>", views.update_inquiry_stage, name="update_inquiry_stage"),
]