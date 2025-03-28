"""
URL configuration for clothline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from myApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.landing, name='landing'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.login_view, name='login'),

    path('login-success/', views.login_success, name='login_success'),

    path('collection/', views.collection_view, name='collection'),

    path('accounts/', include('allauth.urls')),

    path('cart/', views.cart_detail, name='cart_detail'),

    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)