from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

def index(request):

    ##################################################################
    # commented so it doesnt keep making new prods for every refresh #
    ##################################################################

    # Product.objects.create(
    # name        =   "Superman",
    # description =   "Some dork in a cape",
    # image       =   "guardians1.jpg",
    # price       =   6.20,
    # category    =   "Superhero",
    # quantity    =   42
    # )
    context = {
    "products":Product.objects.all()
    }
    return render(request, 'comics/index.html', context)

def admin(request):
    return render(request, 'comics/admin.html')

def admin_login(request):
    if request.method=="POST":
        admin = User.userManager.admin_login(request.POST)
        if 'errors' in admin:
            for error in admin['errors']:
                messages.error(request, error)
            return redirect('/admin')
        else:
            request.session['id'] = admin['admin'].id
            request.session['auth'] = admin['admin'].admin_auth
            context = {
            "users": User.userManager.all()
            }
            return render(request, 'comics/admin_main.html', context)
    return redirect('/admin')

def register(request):
    if request.method=="POST":
        User.userManager.create(
        email       =   request.POST['email'],
        password    =   request.POST['password'],
        first_name  =   request.POST['first_name'],
        last_name   =   request.POST['last_name'],
        admin_auth  =   request.POST['admin'],
        addr_street =   request.POST['addr_street'],
        street_two  =   request.POST['street_two'],
        addr_city   =   request.POST['addr_city'],
        addr_state  =   request.POST['state'],
        addr_zip    =   request.POST['addr_zip']
        )
    return redirect('/admin')

def product_view(request):
    context = {
    "products":Product.objects.all()
    }
    return render(request, 'comics/admin_products.html', context)

def orders_view(request):
    return render(request, 'comics/admin_orders.html')

def products_main(request):
    context = {
        'products' : Product.objects.all()
    }
    return render(request, 'comics/products_main.html', context)

def product_spotlight(request):
    return render(request, 'comics/product_spotlight.html')

def shopping_cart(request):
    return render(request, 'comics/shopping_cart.html')
