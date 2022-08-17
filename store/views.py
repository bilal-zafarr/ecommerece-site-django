import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import *

# Create your views here.


def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("store")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("store")

        else:
            messages.error(request, "store/login_register.html")

    context = {"page": page}
    return render(request, "store/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("store")


def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            customer = Customer.objects.create(
                user=user, name=user.username, email=request.POST.get("email").lower
            )
            login(request, user)
            return redirect("store")
        else:
            messages.error(request, "An error occured during registration")

    context = {"form": form}
    return render(request, "store/login_register.html", context)


def store(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "store/store.html", context)


@login_required(login_url="login")
def cart(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/cart.html", context)


@login_required(login_url="login")
def checkout(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/checkout.html", context)


@login_required(login_url="login")
def updateItem(request, pk):
    # data = json.loads(request.body)
    # productId = data['productId']
    # action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    orderItem.quantity = orderItem.quantity + 1

    # if action == 'add':
    #     orderItem.quantity = (orderItem.quantity + 1)
    # elif action == 'remove':
    #     orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


@login_required
def processOrder(request):
    pass
    # transaction_id = datetime.datetime.now().timestamp()

    # data = json.loads(request.body)

    # if request.user.is_authenticated:
    # 	customer = request.user.customer
    # 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # else:
    # 	customer, order = guestOrder(request, data)

    # total = float(data['form']['total'])
    # order.transaction_id = transaction_id

    # if total == order.get_cart_total:
    # 	order.complete = True
    # order.save()

    # if order.shipping == True:
    # 	ShippingAddress.objects.create(
    # 	customer=customer,
    # 	order=order,
    # 	address=data['shipping']['address'],
    # 	city=data['shipping']['city'],
    # 	state=data['shipping']['state'],
    # 	zipcode=data['shipping']['zipcode'],
    # 	)

    # return JsonResponse('Payment submitted..', safe=False)
