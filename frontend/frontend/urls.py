"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from stroam import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('movies/', views.homeMovies, name='homeMovies'),
    path('series/', views.homeSeries, name='homeSeries'),
    path('movie/<int:id>', views.singleMovie, name='movie-single'),
    path('cart/', views.shoppingCart, name='shopping-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/create', views.checkoutCreate, name='checkoutCreate'),
    path('pay/<slug:checkout_token>', views.pay, name='pay'),
    path('checkout/success', views.paymentCompleted, name='paymentCompleted'),
    path('checkout/error', views.paymentError, name='paymentError'),
    path('userpanel/', views.userPanel, name='user-panel'),
    path('deleteAll', views.deleteAll, name='deleteAll'),
]

# DELETE ALL IS ONLY FOR DEBUGGING PURPOSES, IT DELETES ALL DATA FROM FRONTEND DATABASE + SESSION DATA
