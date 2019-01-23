from django.shortcuts import render
from .models import User
from .models import receipt
from .models import DrugStore
from .forms import UserForm , UserEditForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from .utils import SQLCommand
from .utils import mailPasswordUtils

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


def enter(request):
    if request.method == "POST":
        loginId = request.POST.get("id", "")
        loginPassword = request.POST.get("password", "")

        if SQLCommand.signInSQL(loginId, loginPassword) > 0:
            userRole = loginId[0]
            print(userRole)
            if userRole == '1':
                doctor = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=1')
                return render(request, 'hospitalsite/panelDoctor.html', {'doctor': doctor})
            elif userRole == '2':
                patient = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=2')
                return render(request, 'hospitalsite/panelPatient.html', {'patient': patient})
            elif userRole == '3':
                user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=3')
                return render(request, 'hospitalsite/edit.html', {'user': user})
            elif userRole == '4':
                accountant = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=4')
                return render(request, 'hospitalsite/panelAccountant.html', {'accountant': accountant})
            elif userRole == '5':
                manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
                user = User.objects.raw('SELECT * FROM hospitalsite_user ')
                return render(request, 'hospitalsite/panelManager.html', {'manager': manager , 'user':user})


def verifyUser(request):
    if request.method == "POST":
        verifyId = request.POST.get("id", "")
        verifyPassword = mailPasswordUtils.createRandomPassword()
        verifyEmail = request.POST.get("email", "")
        SQLCommand.VerifyUserSQL(str(verifyId))
        SQLCommand.setUserPassword(verifyId, verifyPassword)
        mailPasswordUtils.sendVerificationMail(verifyEmail, verifyPassword)
        return HttpResponse("Success!")
    return HttpResponse("failed")

def dragStore(request):
    drug = DrugStore.objects.raw('SELECT * FROM hospitalsite_drugStore ')
    return render(request,'hospitalsite/dragStore.html',{'drug':drug})

def managerPanel(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    user = User.objects.raw('SELECT * FROM hospitalsite_user ')
    return render(request, 'hospitalsite/panelManager.html', {'manager': manager, 'user': user})


def doctorPanel(request):
    doctor = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=1')
    return render(request, 'hospitalsite/panelDoctor.html', {'doctor': doctor})


def patientPanel(request):
    patient = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=2')
    return render(request, 'hospitalsite/panelPatient.html', {'patient': patient})


def reseptionPanel(request):
    reseption = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=3')
    return render(request, 'hospitalsite/panelReseption.html', {'reseption': reseption})


def accountantPanel(request):
    accountant = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=4')
    user = User.objects.raw('SELECT * FROM hospitalsite_receipt ')
    return render(request, 'hospitalsite/panelAccountant.html', {'accountant': accountant , 'user':user})

def managerPanel(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    user = User.objects.raw('SELECT * FROM hospitalsite_user ')
    return render(request, 'hospitalsite/panelManager.html', {'manager': manager, 'user': user})


def edit(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    return render(request, 'hospitalsite/edit.html',{'user':user})


def editDoctor(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=1')
    return render(request, 'hospitalsite/edit.html',{'user':user})


def editPatient(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=2')
    return render(request, 'hospitalsite/edit.html',{'user':user})


def editReseption(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=3')
    return render(request, 'hospitalsite/edit.html',{'user':user})


def editAccountant(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=4')
    return render(request, 'hospitalsite/edit.html',{'user':user})


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