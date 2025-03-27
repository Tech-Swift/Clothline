from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm
from .models import Item

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):  # Renamed to avoid conflict with Django's login()
    return render(request, 'login.html')

def collection_view(request):
    item = Item.objects.all()
    return render(request, "collection.html", {"items": item})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('home')  # Redirect to home or dashboard page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})