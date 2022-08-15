from django.shortcuts import render

# Create your views here.


def store(request):
    context = {}
    return render(request, "store/main.html", context)


def cart(request):
    pass


def checkout(request):
    pass
