from django.urls import path
from hospitalsite import views

urlpatterns = [
    # path('', views.hospital, name='hospital'),
    path('', views.signUp, name='signUp'),
    path('signIn/',views.signIn, name='signIn'),
    path('dragStore/',views.dragStore, name='dragStore'),
    path('dragStore/filter/', views.filter, name='filter'),
    path('success/',views.success, name='success'),
    path('signIn/enter/', views.enter, name='enter'),
    path('signIn/enter/sendMessage/', views.sendMessage, name='sendMessage'),
    path('signIn/enter/sendMessage/send/', views.send, name='send'),
    path('signIn/enter/showMessage/', views.showMessage, name='showMessage'),
    path('signIn/enter/verifyUser/', views.verifyUser, name='verifyUser'),
    path('managerPanel/', views.managerPanel, name='managerPanel'),
    path('signIn/enter/edit/', views.edit, name='edit'),
    path('managerPanel/edit/editSuccess/', views.editSuccess, name='editSuccess'),
    path('doctorPanel/', views.doctorPanel, name='doctorPanel'),
    path('patientPanel/', views.patientPanel, name='patientPanel'),
    path('reseptionPanel/', views.reseptionPanel, name='reseptionPanel'),
    path('accountantPanel/', views.accountantPanel, name='accountantPanel'),
    path('signIn/enter/editDoctor/', views.editDoctor, name='editDoctor'),
    path('signIn/enter/editPatient/', views.editPatient, name='editPatient'),
    path('signIn/enter/editReseption/', views.editReseption, name='editReseption'),
    path('signIn/enter/editAccountant/', views.editAccountant, name='editAccountant'),

]