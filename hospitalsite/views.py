from django.shortcuts import render
from .models import User
from .models import DrugStore
from .forms import UserForm
from django.shortcuts import redirect


# Create your views here.

# def hospital(request):
#     drugs = DrugStore.objects.filter(expiredDate='1398')
#     return render(request, 'hospitalsite/hospital.html', {'drugs': drugs})


def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name =str( request.user)
            user.id = request.user
            user.save()
    else:
        form = UserForm()
    return render(request, 'hospitalsite/hospital.html', {'form': form})