from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import *
from django.contrib import messages
from forms import SalePaymentForm
from django.views.decorators.csrf import csrf_exempt
import re
NO_LET_REGEX = re.compile(r'^-?[0-9]+$')
def add_test(request):
    # ============== #
    # ADD QUERY HERE #
    # ============== #
    # Add category
    # Category.objects.create(
    #     name = 'Category1'
    # )
    # Category.objects.create(
    #     name = 'Category2'
    # )
    # Category.objects.create(
    #     name = 'Category3'
    # )

    # Add Product
    # Product.productManager.create(
    #     name='ProductThree',
    #     description='the desc',
    #     image = 'guardians1.jpg',
    #     price = 91.10,
    #     quantity = 5,
    # )
    # category = Category.objects.get(name='Category2')
    # product = Product.productManager.get(name='ProductThree')
    # category.products.add(product)

    return redirect('/test')
def test(request):
    # ============== #
    # ADD QUERY HERE #
    # ============== #
    # products = Product.productManager.all()
    context = {
        'categories' : Category.objects.all(),
        'products' : Product.productManager.all()
    }
    return render(request,'comics/test.html', context)

def index(request):

    ##################################################################
    # commented so it doesnt keep making new prods for every refresh #
    ##################################################################

    # Product.productManager.create(
    # name        =   "Superman",
    # description =   "Some dork in a cape",
    # image       =   "guardians1.jpg",
    # price       =   6.20,
    # category    =   "Superhero",
    # quantity    =   42
    # )
    context = {
    "products":Product.productManager.all()
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
    "products":Product.productManager.all()
    }
    return render(request, 'comics/admin_products.html', context)

def orders_view(request):
    return render(request, 'comics/admin_orders.html')

def products_main(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    context = {
        'products' : Product.productManager.all(),
        'categories' : Category.objects.all(),
     }
    return render(request, 'comics/products_main.html', context)
def product_category(request,category_id):
    context = {
        'products' : Product.productManager.filter(product_categories__id= category_id)
    }
    return render(request,'comics/prod_category.html', context)

def product_spotlight(request):
    return render(request, 'comics/product_spotlight.html')

def shopping_cart(request):
    return render(request, 'comics/shopping_cart.html')

def product_adder(request):
    if request.method=="POST":
        product = Product.productManager.validate_product(request.POST)
        if 'errors' in product:
            for error in product['errors']:
                messages.error(request, error)
                return redirect('/product_adder')
        if 'the_product' in product:
            messages.success(request, "Successfully added product!")
            return redirect('/dashboard/products')
    return redirect('/dashboard/products')

# ============== #
# === STRIPE === #
# ============== #
@csrf_exempt
def charge(request,order_id):
    context = {
        'order_id' : order_id
    }
    # if 'total' not in request.session:
    #     request.session['total'] = 300
    # request.session['total'] = 4000
    # # the_amount = request.session['total']
    # # print the_amount
    # if request.method == "POST":
    #     # total = charge_me(10000)
    #     form = SalePaymentForm(request.POST)
    #
    #     if form.is_valid(): # charges the card
    #         sale = Sale()
    #         sale.charge(100000,4242424242424242,01,2019,424)
    #         return HttpResponse("Success! We've charged your card!")
    # else:
    #     form = SalePaymentForm()

    return render(request , "includes/card.html" , context)

def charge_process(request,order_id):
    if request.method == 'POST':
        # sale = sale()
        # card = sale.validate_card(request.POST)
        if not NO_LET_REGEX.match(request.POST['number']):
            # error.msgs.append('Card Number invalid')
            messages.error(request,'Card Number invalid')
            return redirect('/charge/' + str(order_id))
        if len(request.POST['number']) != 16:
            # error.msgs.append('Card number invalid')
            messages.error(request,'Card number invalid')
            return redirect('/charge/' + str(order_id))
        if len(request.POST['cvc']) != 3:
            # error.msgs.append('CVC is invalid')
            messages.error(request,'CVC is invalid')
            return redirect('/charge/' + str(order_id))

        # if 'errors' in card:
        #     for error in card['errors']:
        #         messages.error(request,error)
        #     return redirect('/charge/' + str(order_id))
        # if 'validated_card' in card:
        sale = Sale()
        sale.charge(99999999,request.POST['number'],request.POST['exp_month'],request.POST['exp_year'],request.POST['cvc'])
        return redirect('/')

# ===================== #
# === END OF STRIPE === #
# ===================== #
