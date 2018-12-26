from django.shortcuts import render
from .models import User
from .models import DrugStore
from .forms import UserForm
from django.shortcuts import redirect
from django.http import HttpResponse


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
        print("hi")
        if form.is_valid():
            user = User(name=str(form.cleaned_data['name']), id=str(form.cleaned_data['id']), tel=str(form.cleaned_data['tel']), Email=str(form.cleaned_data['Email']))
            print("name: " + form.cleaned_data['name'])
            user.save()


    return HttpResponse("Success!")
