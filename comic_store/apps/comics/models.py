from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CHAR_DIGIT_REGEX = re.compile(r'^[a-zA-Z0-9_.-]*$')
CATEGORY_REGEX = re.compile(r'^[A-Za-z]*$')
PRICE_REGEX = re.compile(r'^(?!0+(\.0+)?$)\d{0,5}(.\d{1,2})?$')

class UserManager(models.Manager):
    def admin_login(self, post_data):
        error_msgs = []
        if User.userManager.get(email=post_data['email']) and User.userManager.get(email=post_data['email']).admin_auth:
            stored_pw = User.userManager.get(email=post_data['email']).password
            if stored_pw == post_data['password']:
                return {"admin": User.userManager.get(email=post_data['email'])}
            else:
                error_msgs.append("Invalid Login")
                return {"errors":error_msgs}
        else:
            error_msgs.append("Invalid Login")
            return {"errors":error_msgs}

        def user_login(self, post_data):
            error_msgs = []
            if User.userManager.get(email=post_data['email']):
                stored_pw = User.userManager.get(email=post_data['email']).password
                if stored_pw == post_data['password']:
                    return {"theuser": User.userManager.get(email=post_data['email'])}
                else:
                    error_msgs.append("Invalid Login")
                    return {"errors":error_msgs}
            else:
                error_msgs.append("Invalid Login")
                return {"errors":error_msgs}

class OrderManager(models.Manager):
    def create_order(self, post_data, product_ids):
        # create user based on billing information
        u_fname = post_data['u_fname']
        u_lname = post_data['u_lname']
        u_addr_street = post_data['u_addr_street']
        u_street_two = post_data['u_street_two']
        u_addr_city = post_data['u_addr_city']
        u_addr_state = post_data['u_addr_state']
        u_addr_zip = post_data['u_addr_zip']
        the_user = User.objects.create(first_name=u_fname, last_name=u_lname, addr_street=u_addr_street, street_two=u_street_two, addr_city=u_addr_city, addr_state=u_addr_state, addr_zip=u_addr_zip)
        # shipping information
        addr_street = post_data['addr_street']
        street_two = post_data['street_two']
        addr_city = post_data['addr_city']
        addr_state = post_data['addr_state']
        the_order = Order.orderManager.create(addr_street=addr_street, street_two=street_two, addr_city=addr_city, addr_state=addr_state)
        the_order.user.add(the_user)
        for product_id in product_ids:
            # add product to order object
            the_product = Product.productManager.get(id=product_id)
            the_order.products.add(the_product)
        # depending on what we return, change this following line
        return {'the_order': the_order}

class ProductManager(models.Manager):
    def validate_product(self, post_data, submitted_image):
        error_msgs = []
        p_name = post_data['p_name']
        p_description = post_data['p_description']
        if 'p_category' in post_data:
            p_category = post_data['p_category']
        new_p_category = post_data['new_p_category']
        p_price = Decimal(post_data['p_price'])
        p_quantity = int(post_data['p_quantity'])
        print submitted_image
        if len(p_name) < 2:
            error_msgs.append('Product name must be 2 or more characters')
        elif not CHAR_DIGIT_REGEX.match(p_name):
            error_msgs.append('Invalid product name')
        if len(p_description) < 1:
            error_msgs.append('Product description cannot be blank')
        if not CATEGORY_REGEX.match(new_p_category):
            error_msgs.append('Invalid category')
        # price form
        if p_price < 0:
            error_msgs.append('Cannot have negative price')
        elif p_price >= 1000:
            error_msgs.append('Price must be between $0 and $999.99')
        if not submitted_image:
            error_msgs.append('You failed to upload a picture')
        if new_p_category:
            category = new_p_category
        else:
            category = p_category
        # regex for price
        # elif not PRICE_REGEX.match(p_price):
        #     error_msgs.append('Invalid price')
        if error_msgs:
            return {'errors': error_msgs}
        else:
            # create product
            if new_p_category:
                new_cat = Category.objects.create(name=category)
                the_product = Product.productManager.create(name=p_name, description=p_description, image=submitted_image, price=p_price, quantity=p_quantity, category=new_cat)
            else:
                old_cat = Category.objects.get(name=category)
                the_product = Product.productManager.create(name=p_name, description=p_description, image=submitted_image, price=p_price, quantity=p_quantity, category=old_cat)
            # depending on what we return
            return {'the_product': the_product}

    def update_product(self, post_data, product_id):
        error_msgs = []
        new_name = post_data['edit_name']
        new_desc = post_data['edit_description']
        if 'edit_category' in post_data:
            edit_category = post_data['edit_category']
        new_edit_category = post_data['new_edit_category']
        new_price         = post_data['edit_price']
        new_quantity      = post_data['edit_quantity']
        if new_edit_category:
            new_cat = Category.objects.create(name=new_edit_category)
            Product.productManager.filter(id=product_id).update(name=new_name, description=new_desc, price=new_price, quantity=new_quantity, category=new_cat)
        else:
            old_category = Category.objects.get(name=edit_category)
            Product.productManager.filter(id=product_id).update(name=new_name, description=new_desc, price=new_price, quantity=new_quantity, category=old_category)


# class OrderManager(models.Manager):
#    def create_order(self, post_data, user_id):
#        the_user = User.objects.get(id=user_id)
#
#    def add_to_order(self, post_data, user_id):

class User(models.Model):
    email       =   models.CharField(max_length=100, default=None)
    password    =   models.CharField(max_length=100, default=None)
    first_name  =   models.CharField(max_length=60)
    last_name   =   models.CharField(max_length=60)
    admin_auth  =   models.BooleanField(default=False)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    userManager =   UserManager()

class Category(models.Model):
    name        =   models.CharField(max_length=60)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)

class Product(models.Model):
    name        =   models.CharField(max_length=60)
    description =   models.TextField(max_length=1000)
    image       =   models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    price       =   models.DecimalField(max_digits=5,decimal_places=2)
    quantity    =   models.IntegerField(default=0)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    category    =   models.ForeignKey(Category, related_name="product_category", default=None)
    productManager = ProductManager()

class Order(models.Model):
    products    =   models.ManyToManyField(Product, related_name="product_orders")
    user        =   models.ForeignKey(User, related_name="user_orders")
    s_fname     =   models.CharField(max_length=60, default=None)
    s_lname     =   models.CharField(max_length=60, default=None)
    total       =   models.DecimalField(max_digits=5,decimal_places=2)
    status      =   models.IntegerField(default=0)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    orderManager = OrderManager()

class Location(models.Model):
    addr_street =   models.CharField(max_length=100)
    street_two  =   models.CharField(max_length=100)
    addr_city   =   models.CharField(max_length=100)
    addr_state  =   models.CharField(max_length=20)
    addr_zip    =   models.IntegerField()
    user        =   models.OneToOneField(User, related_name='user_location')
    order       =   models.OneToOneField(Order, related_name='shipping_location')
