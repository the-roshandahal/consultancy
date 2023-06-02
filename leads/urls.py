from django.urls import path
from django.urls import re_path
from .import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static 

urlpatterns = [
    
    path("crm_setup/", views.crm_setup, name="crm_setup"),
    path("create_stage/", views.create_stage, name="create_stage"),
    path("edit_stage/<int:id>", views.edit_stage, name="edit_stage"),
    path("create_source/", views.create_source, name="create_source"),
    path("edit_source/<int:id>", views.edit_source, name="edit_source"),
    path("delete_stage/<int:id>", views.delete_stage, name="delete_stage"),
    path("delete_source/<int:id>", views.delete_source, name="delete_source"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
