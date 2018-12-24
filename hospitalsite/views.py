from django.shortcuts import render
from .models import User
from .models import DrugStore
from .forms import UserForm
from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.

# def hospital(request):
#     drugs = DrugStore.objects.filter(expiredDate='1398')
#     return render(request, 'hospitalsite/hospital.html', {'drugs': drugs})

def signin(request):
    return render(request,'hospitalsite/signin.html')

def login(request):
    return render(request, 'hospitalsite/hospital.html')


def success(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(id=44, name=str(form.cleaned_data['name']))
            print("name: " + form.cleaned_data['name'])
            user.save()

    return HttpResponse("Success!")
