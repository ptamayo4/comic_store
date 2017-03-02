from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

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
    if 'product_ids' not in request.session:
        request.session['product_ids'] = {}
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

def display_test(request):
    # stop creating the the best product
    #Product.productManager.create(name='Superman 1 1939', description='Worth over a million dollars', image='superman', price=100.00, quantity=1)

    # stop creating the user
    #User.userManager.create(first_name='Brian', last_name='Sung', email='thisiscool@gmail.com', password='Thisisapassword')

    #the_user = User.userManager.get(id=2)
    the_order = Order.orderManager.get(id=1)
    the_product = Product.productManager.get(id=10)
    #the_order = Order.orderManager.create(s_fname='Dan', s_lname='Smith', total=4.00, user=the_user, status=0)
    the_order.products.add(the_product)
    the_order.save()
    context = {
            'order': the_order,
            'products': Product.productManager.all(),
            'order_products': the_order.products.all()
            }
    return render(request, 'comics/product_test.html', context)
