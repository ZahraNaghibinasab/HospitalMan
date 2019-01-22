from django.shortcuts import render
from .models import User
from .models import DrugStore
from .forms import UserForm , UserEditForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from .utils import SQLCommand

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
    return render(request, 'hospitalsite/panelManager.html', {'manager': manager})

def edit(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    return render(request, 'hospitalsite/edit.html',{'manager':manager})

def editSuccess(request):
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            cursor.execute('UPDATE hospitalsite_user \
            SET name=COALESCE(%s, name), \
            tel=COALESCE(%s, tel), \
            weight=COALESCE(%s, weight) , \
            height=COALESCE(%s, height), \
            gender=COALESCE(%s, gender), \
            age=COALESCE(%s, age), \
            address=COALESCE(%s, address), \
            postalCode=COALESCE(%s, postalCode) \
            WHERE role=5',[str(form.cleaned_data['name']),
            str(form.cleaned_data['tel']),
            (form.cleaned_data['weight']),
            (form.cleaned_data['height']),
            (form.cleaned_data['gender']),
            (form.cleaned_data['age']),
            str(form.cleaned_data['address']),
            str(form.cleaned_data['postalCode'])])


    return HttpResponse("Success!")