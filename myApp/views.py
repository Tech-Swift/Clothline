from multiprocessing import AuthenticationError
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from clothline.settings import AUTHENTICATION_BACKENDS

from .forms import SignupForm
from .models import Item
from django.contrib.auth import login, authenticate
# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):  # Renamed to avoid conflict with Django's login()
    return render(request, 'login.html')

def login_success(request):
    return redirect("collection") 


def collection_view(request):
    item = Item.objects.all()
    return render(request, "collection.html", {"items": item})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash password
            user.save()

            # Authenticate user after signup
            user = authenticate(request, username=user.email, password=form.cleaned_data['password1'])
            if user:
                login(request, user)
                return redirect("collection")  # Redirect to collection page after signup
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = SignupForm()
    
    return render(request, "signup.html", {"form": form})
 