from django.shortcuts import render
from .models import User
from .models import DrugStore


# Create your views here.

def hospital(request):
    drugs = DrugStore.objects.filter(expiredDate='1398')
    return render(request, 'hospitalsite/hospital.html', {'drugs': drugs})
