from multiprocessing import AuthenticationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Customer, Cart, CartItem, Item, Wishlist


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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to add items to the cart'}, status=401)

    item = get_object_or_404(Item, id=item_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = CartItem.objects.filter(cart=cart).count()

    return JsonResponse({'message': 'Item added to cart!', 'cart_count': cart_count})


@login_required
def cart_detail(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }
    )

    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cartitem_set.all() if cart else []
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)

        customer, created = Customer.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += 1  # Increase quantity if item already exists
            cart_item.save()

        cart_count = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({'message': 'Item added to cart!', 'cart_count': cart_count})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    cart_count = CartItem.objects.filter(cart=cart_item.cart).count()

    return JsonResponse({'message': 'Item removed from cart!', 'cart_count': cart_count})


@login_required
def add_to_wishlist(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.add(item)

        return JsonResponse({'message': 'Item added to wishlist!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)
