from django.shortcuts import render
from .models import User
from .models import receipt
from .models import DrugStore
from .models import Reservation
from .models import Prescription
from .forms import UserForm, UserEditForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from .utils import SQLCommand
from .utils import mailPasswordUtils

signInUserID = ""

patientID = ""


# Create your views here.

# def hospital(request):
#     drugs = DrugStore.objects.filter(expiredDate='1398')
#     return render(request, 'hospitalsite/signUp.html', {'drugs': drugs})
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def signIn(request):
    return render(request, 'hospitalsite/signIn.html')


def signUp(request):
    return render(request, 'hospitalsite/signUp.html')


def success(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            cursor.execute('INSERT INTO hospitalsite_user (name , id , tel , Email) VALUES (%s , %s , %s , %s) ',
                           [str(form.cleaned_data['name']), str(form.cleaned_data['id']), str(form.cleaned_data['tel']),
                            str(form.cleaned_data['Email'])]
                           )
            userid = request.POST.get("id", "")
            userRole = userid[0]
            print(userid)
            cursor.execute('UPDATE hospitalsite_user SET role = %s WHERE id = %s', [userRole, userid])

            if userRole == '1':
                cursor.execute('INSERT into hospitalsite_doctor (idD_id) VALUES (%s)', [userid])
            elif userRole == '2':
                cursor.execute('INSERT into hospitalsite_patient (idP_id) VALUES (%s)', [userid])
            elif userRole == '3':
                cursor.execute('INSERT into hospitalsite_reception (idR_id) VALUES (%s)', [userid])
            elif userRole == '4':
                cursor.execute('INSERT into hospitalsite_accountant (idA_id) VALUES (%s)', [userid])
            elif userRole == '5':
                cursor.execute('INSERT into hospitalsite_manager (idM_id) VALUES (%s)', [userid])

    return HttpResponse("Success!")


def enter(request):
    if request.method == "POST":
        loginId = request.POST.get("id", "")
        loginPassword = request.POST.get("password", "")
        global signInUserID
        signInUserID = loginId
        if SQLCommand.signInSQL(loginId, loginPassword) > 0:
            userRole = loginId[0]
            print(userRole)
            if userRole == '1':
                doctorTable = SQLCommand.DoctorRsvTable(signInUserID)
                doctor = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [loginId])
                return render(request, 'hospitalsite/panelDoctor.html', {'doctor': doctor, 'doctorTable': doctorTable})
            elif userRole == '2':
                patient = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [loginId])
                idP = SQLCommand.getPatientID(loginId)
                drug = SQLCommand.getPatientDrugNames(idP)
                reserve = SQLCommand.PatientRsvTable()
                return render(request, 'hospitalsite/panelPatient.html',
                              {'patient': patient, 'drug': drug, 'reserve': reserve})
            elif userRole == '3':
                user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [loginId])
                idPatient = Reservation.objects.raw('SELECT idP_id FROM hospitalsite_reservation')
                idPshow = SQLCommand.getP(idPatient)
                idDoctor = Reservation.objects.raw('SELECT idD_id FROM hospitalsite_reservation')
                idDshow = SQLCommand.getD(idDoctor)
                namePatient = SQLCommand.getNameP(idPshow)
                nameDoctor = SQLCommand.getNameD(idDshow)
                reserve = SQLCommand.getReceptionTable(idDoctor, idDshow, idPatient, idPshow, nameDoctor, namePatient)
                return render(request, 'hospitalsite/panelReseption.html', {'reseption': user, 'reserve': reserve})
            elif userRole == '4':
                accountant = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [loginId])
                return render(request, 'hospitalsite/panelAccountant.html', {'accountant': accountant})
            elif userRole == '5':
                manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [loginId])
                user = User.objects.raw('SELECT * FROM hospitalsite_user ')
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM django_admin_log')
                log = dictfetchall(cursor)
                return render(request, 'hospitalsite/panelManager.html', {'manager': manager, 'user': user, 'log': log})
        else:
            return HttpResponse("You are not registered!")


def verifyUser(request):
    if request.method == "POST":
        # Verify button is clicked
        print("button: " + request.POST.get("button", ""))
        if request.POST.get("button", "") == "Verify":
            verifyId = request.POST.get("id", "")
            verifyPassword = mailPasswordUtils.createRandomPassword()
            verifyEmail = request.POST.get("email", "")
            SQLCommand.VerifyUserSQL(str(verifyId))
            SQLCommand.setUserPassword(verifyId, verifyPassword)
            mailPasswordUtils.sendVerificationMail(verifyEmail, verifyPassword)
            return HttpResponse("User Verified!")
        # Delete button is clicked
        elif request.POST.get("button", "") == "Delete":
            deleteId = request.POST.get("id", "")
            SQLCommand.deleteUserSQL(deleteId)
            return HttpResponse("User Deleted!")

    return HttpResponse("failed")


def dragStore(request):
    drug = DrugStore.objects.raw('SELECT * FROM hospitalsite_drugStore ')
    return render(request, 'hospitalsite/dragStore.html', {'drug': drug})


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
    idPatient = Reservation.objects.raw('SELECT idP_id FROM hospitalsite_reservation')
    idPshow = SQLCommand.getP(idPatient)
    idDoctor = Reservation.objects.raw('SELECT idD_id FROM hospitalsite_reservation')
    idDshow = SQLCommand.getD(idDoctor)
    namePatient = SQLCommand.getNameP(idPshow)
    nameDoctor = SQLCommand.getNameD(idDshow)
    reserve = SQLCommand.getReceptionTable(idDoctor, idDshow, idPatient, idPshow, nameDoctor, namePatient)
    return render(request, 'hospitalsite/panelReseption.html', {'reseption': reseption, 'reserve': reserve})


def accountantPanel(request):
    accountant = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=4')
    user = User.objects.raw('SELECT * FROM hospitalsite_receipt ')
    return render(request, 'hospitalsite/panelAccountant.html', {'accountant': accountant, 'user': user})


def managerPanel(request):
    manager = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
    user = User.objects.raw('SELECT * FROM hospitalsite_user ')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM django_admin_log')
    log = dictfetchall(cursor)
    return render(request, 'hospitalsite/panelManager.html', {'manager': manager, 'user': user, 'log': log})


# def edit(request):
#     user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=5')
#     return render(request, 'hospitalsite/edit.html',{'user':user})

def edit(request):
    user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE id = %s ', [signInUserID])
    return render(request, 'hospitalsite/edit.html', {'user': user})


#
# def editDoctor(request):
#     user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=1')
#     return render(request, 'hospitalsite/edit.html',{'user':user})
#
#
# def editPatient(request):
#     user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=2')
#     return render(request, 'hospitalsite/edit.html',{'user':user })
#
#
# def editReseption(request):
#     user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=3')
#     return render(request, 'hospitalsite/edit.html',{'user':user})
#
#
# def editAccountant(request):
#     user = User.objects.raw('SELECT * FROM hospitalsite_user WHERE role=4')
#     return render(request, 'hospitalsite/edit.html',{'user':user})
#

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
            WHERE role=5', [str(form.cleaned_data['name']),
                            str(form.cleaned_data['tel']),
                            (form.cleaned_data['weight']),
                            (form.cleaned_data['height']),
                            (form.cleaned_data['gender']),
                            (form.cleaned_data['age']),
                            str(form.cleaned_data['address']),
                            str(form.cleaned_data['postalCode'])])

    return HttpResponse("Success!")


def filter(request):
    if request.method == "POST":
        drugDate = request.POST.get("expiredDate", "")
        print("drugdate: " + str(drugDate))
        drugNameID = SQLCommand.filterDrugs(drugDate)
        print(drugNameID)
        return render(request, 'hospitalsite/filter.html', {'drugNameID': drugNameID})


def sendMessage(request):
    return render(request, 'hospitalsite/sendMessage.html')


def send(request):
    if request.method == "POST":
        role = signInUserID[0]
        pId = request.POST.get("patientId", "")
        dId = request.POST.get("doctorId", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        patientId = SQLCommand.getPatientID(pId)
        doctorId = SQLCommand.getDoctorID(dId)
        SQLCommand.insertMessage(patientId, doctorId, subject, message, role)
        return HttpResponse("Your message has been sent. please sign in again!")
    else:
        return HttpResponse("Failed!")


def showMessage(request):
    print("this:")
    print(signInUserID)
    role = signInUserID[0]
    if role == '1':
        idD = SQLCommand.reverseDoctorId(signInUserID)
        messages = SQLCommand.getDoctorMessage(idD)
    elif role == '2':
        idP = SQLCommand.reversePatientId(signInUserID)
        messages = SQLCommand.getPatientMessage(idP)
    return render(request, 'hospitalsite/showMessage.html', {'messages': messages})


def forgotPassword(request):
    return render(request, 'hospitalsite/forgotPassword.html')


def sendPassword(request):
    if request.method == "POST":
        userEmail = request.POST.get("email", "")
        userPassword = SQLCommand.getUserPassword(userEmail)
        mailPasswordUtils.sendForgottenPassword(userEmail, userPassword)
        return HttpResponse("Success!")

    else:
        return HttpResponse("Failed!")


def cancel(request):
    return HttpResponse("Your patient is canceled!")


def accept(request):
    return HttpResponse("Your patient is accepted!")


def reserveDoctor(request):
    if request.method == "POST":
        global signInUserID
        row = request.POST.get("id", "")
        patientId = SQLCommand.getPatientID(signInUserID)
        SQLCommand.reserveTimeByPatient(row, patientId)
        return HttpResponse("Successfully reserved!")
    else:
        return HttpResponse("Reserve failed!")
