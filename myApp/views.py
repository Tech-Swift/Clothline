from multiprocessing import AuthenticationError
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from clothline.settings import AUTHENTICATION_BACKENDS

from .forms import SignupForm
from .models import Cart, CartItem, Customer, Item
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

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    customer = request.user.customer  # Assuming a logged-in user has a related Customer profile
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')
def cart_detail(request):
    user = request.user

    # Ensure the user has a related Customer instance
    customer, created = Customer.objects.get_or_create(
        user=user,
        defaults={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    )

    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cartitem_set.all() if cart else []

    return render(request, 'cart_detail.html', {'cart_items': cart_items})


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')
 