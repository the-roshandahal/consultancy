from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("inquiry/", views.inquiry, name="inquiry"),
    path("inquiry_setup/", views.inquiry_setup, name="inquiry_setup"),
    path("my_inquiries/", views.my_inquiries, name="my_inquiries"),
    path("active_inquiries/", views.active_inquiries, name="active_inquiries"),


    path("inactive_inquiry/", views.inactive_inquiry, name="inactive_inquiry"),
    path("add_inquiry/", views.add_inquiry, name="add_inquiry"),
    path("view_inquiry/<int:id>", views.view_inquiry, name="view_inquiry"),
    path("add_inquiry_note/<int:id>", views.add_inquiry_note, name="add_inquiry_note"),
    path("update_inquiry_stage/<int:id>", views.update_inquiry_stage, name="update_inquiry_stage"),
    path("edit_inquiry/<int:id>", views.edit_inquiry, name="edit_inquiry"),
    path("add_consultation_date/<int:id>", views.add_consultation_date, name="add_consultation_date"),
    path("delete_inquiry/<int:id>", views.delete_inquiry, name="delete_inquiry"),
    path("close_inquiry/<int:id>", views.close_inquiry, name="close_inquiry"),
    path("reopen_inquiry/<int:id>", views.reopen_inquiry, name="reopen_inquiry"),
    path("external_inquiry", views.external_inquiry, name="external_inquiry"),
]