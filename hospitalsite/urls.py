from django.urls import path
from hospitalsite import views

urlpatterns = [
    # path('', views.hospital, name='hospital'),
    path('', views.signUp, name='signUp'),
    path('signIn/',views.signIn, name='signIn'),
    path('success/',views.success, name='success'),
    path('managerPanel/', views.managerPanel, name='managerPanel'),
    path('managerPanel/edit/', views.edit, name='edit'),

]