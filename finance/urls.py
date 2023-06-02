from django.urls import re_path
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  
from .import views


urlpatterns = [
    path("invoice/", views.invoice, name="invoice"),
    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)