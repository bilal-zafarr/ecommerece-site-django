from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("add-item/<str:pk>", views.addItem, name="add-item"),
    path("remove-item/<str:pk>", views.removeItem, name="remove-item"),
]
