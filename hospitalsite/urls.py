from django.urls import path
from hospitalsite import views

urlpatterns = [
    path('', views.hospital, name='hospital'),
]