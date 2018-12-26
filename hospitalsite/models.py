from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    Email = models.CharField(max_length=60, blank=True, null=True)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=15, blank=True, null=True)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=20)
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

class DrugStore(models.Model):
    idDrug = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    expiredDate = models.CharField(max_length=11)



