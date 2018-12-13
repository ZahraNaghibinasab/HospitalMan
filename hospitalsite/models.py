from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    Email = models.CharField(max_length=60)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    role = models.IntegerField()
    # 0 for doctor
    # 1 for patient
    # 2 for reception
    # 3 for nurse
    # 4 for accountant
    # 5 for manager
    weight = models.FloatField()
    height = models.IntegerField()
    gender = models.IntegerField()
    # 0 for  men
    # 1 for women
    # 2 for others
    age = models.IntegerField()
    address = models.TextField()
    postalCode = models.CharField(max_length=10)


class Manager(models.Model):
    idM = models.ForeignKey(User,on_delete=models.CASCADE)

class Doctor(models.Model):
    idD = models.ForeignKey(User,on_delete=models.CASCADE)

class Nurse(models.Model):
    idN = models.ForeignKey(User,on_delete=models.CASCADE)

class Accountant(models.Model):
    idA = models.ForeignKey(User,on_delete=models.CASCADE)

class Reception(models.Model):
    idR = models.ForeignKey(User,on_delete=models.CASCADE)

class Patient(models.Model):
    idP = models.ForeignKey(User,on_delete=models.CASCADE)

