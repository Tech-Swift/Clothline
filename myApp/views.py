from django.shortcuts import render
from .models import Item

# Create your views here.
def landing(request):
    return render(request, 'landing.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def collection_view(request):
    item = Item.objects.all()
    return render(request, "collection.html", {"items": item})