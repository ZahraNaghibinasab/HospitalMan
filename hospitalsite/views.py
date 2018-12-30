from django.shortcuts import render
from .models import User
from .models import DrugStore
from .forms import UserForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection

# Create your views here.

# def hospital(request):
#     drugs = DrugStore.objects.filter(expiredDate='1398')
#     return render(request, 'hospitalsite/signUp.html', {'drugs': drugs})

def signIn(request):
    return render(request,'hospitalsite/signIn.html')

def signUp(request):
    return render(request, 'hospitalsite/signUp.html')


def success(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            cursor.execute('INSERT INTO hospitalsite_user (name , id , tel , Email) VALUES (%s , %s , %s , %s) ', [str(form.cleaned_data['name']), str(form.cleaned_data['id']),str(form.cleaned_data['tel']), str(form.cleaned_data['Email'])]
)


    return HttpResponse("Success!")

def managerPanel(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    print(manager)
    return render(request, 'hospitalsite/panelManager.html', {'manager': manager})

def edit(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    return render(request, 'hospitalsite/edit.html',{'manager':manager})