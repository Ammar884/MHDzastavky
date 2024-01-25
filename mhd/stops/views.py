from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Station
from .forms import StationForm



def index(request):
    stations = Station.objects.filter(user_id=request.user.id)
    return render(request, "index.html", {"stations": stations})

def registration(request):
    if request.method == "POST":
        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
        
    return render(request, "registration/registration.html", {"form": form})


@login_required
def add_item(request):
    if request.method == "POST":
        form = StationForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.INFO, "Zastávka byla přidána")
            return redirect("index") #zmenit pozdeji na stránku zastávky(zatím neexistuje 16.1.2024)
    else:
        form = StationForm()
    return render(request, "add_item.html", {"form": form})
