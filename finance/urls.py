from django.urls import re_path
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  
from .import views


urlpatterns = [
    path("invoice/", views.invoice, name="invoice"),
    path("create_invoice/", views.create_invoice, name="create_invoice"),   
    path("view_invoice/<int:id>", views.view_invoice, name="view_invoice"),
    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)