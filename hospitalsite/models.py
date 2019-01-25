from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    Email = models.CharField(max_length=60, blank=True, null=True)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=15, blank=True, null=True)
    verified = models.BooleanField(default=False, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    # 1 for doctor
    # 2 for patient
    # 3 for reception
    # 4 for accountant
    # 5 for manager
    weight = models.FloatField( blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    # 0 for  men
    # 1 for women
    # 2 for others
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postalCode = models.CharField(max_length=10, blank=True, null=True)


class Manager(models.Model):
    idM = models.ForeignKey(User,on_delete=models.CASCADE)

class Doctor(models.Model):
    idD = models.ForeignKey(User,on_delete=models.CASCADE)

class Accountant(models.Model):
    idA = models.ForeignKey(User,on_delete=models.CASCADE)

class Reception(models.Model):
    idR = models.ForeignKey(User,on_delete=models.CASCADE)

class Patient(models.Model):
    idP = models.ForeignKey(User,on_delete=models.CASCADE)
    bed = models.BooleanField(default= False)
    # bedId =  models.ForeignKey(Bed,on_delete=models.CASCADE)

class Bed(models.Model):
    id = models.IntegerField(primary_key=True)
    buildingNum =  models.IntegerField()
    hallNum =  models.IntegerField()
    roomNum =  models.IntegerField()

class DrugStore(models.Model):
    idDrug = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    expiredDate = models.CharField(max_length=11)

class receipt(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    subject = models.CharField(max_length=15)
    price = models.IntegerField()


class Reservation(models.Model):
    idD = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.DateTimeField()
    idP = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    checked = models.BooleanField(default=False)

class Prescription(models.Model):
    idPatient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    idDrug = models.ForeignKey(DrugStore, on_delete=models.CASCADE)

class message(models.Model):
    idPatient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    idDoctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)
    text = models.TextField()
    fromPatient = models.BooleanField(default=True)