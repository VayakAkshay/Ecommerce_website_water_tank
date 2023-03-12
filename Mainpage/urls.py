"""Myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.Homepage,name="Homepage"),
    path('about/',views.AboutPage,name="AboutPage"),
    path('products/',views.ProductPage,name="ProductPage"),
    path('myproduct/<id>',views.MyProduct,name="MyProduct"),
    path('search/',views.SearchPage,name="SearchPage"),
    path('contact/',views.ContactPage,name="ContactPage"),
    path('cart/',views.CartPage,name="CartPage"),
    path('profile/',views.ProfilePage,name="ProfilePage"),
    path('deleteitem/',views.DeleteItem,name="DeleteItem"),
    path('vertical/',views.VerticalPro,name="VerticalPro"),
    path('horizontal/',views.HorizontalPro,name="HorizontalPro"),
    path('orders/',views.MyordersPage,name="MyordersPage"),
    path('wishlist/',views.WishlistPage,name="WishlistPage"),
    path('removeitem/',views.RemoveItem,name="RemoveItem"),
    path('order/',views.OrderPage,name="OrderPage"),
    path('checkout/',views.checkout,name="checkout"),
    path('success/',views.success_page,name="success_page"),
    path('cancle/',views.cancle_page,name="cancle_page"),
    path('edit-profile/',views.EditProfile,name="EditProfile"),
    path('Review-page/',views.ReviewHandle,name="ReviewHandle"),
    path('logout/',views.Logout,name="Logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)