from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
import re
import bcrypt
# import settings
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CHAR_DIGIT_REGEX = re.compile(r'^[a-zA-Z0-9_.-]*$')
CATEGORY_REGEX = re.compile(r'^[A-Za-z]*$')
PRICE_REGEX = re.compile(r'^(?!0+(\.0+)?$)\d{0,5}(.\d{1,2})?$')
NO_LET_REGEX = re.compile(r'^[a-zA-Z]+$')
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
    def validate_product(self, post_data):
        error_msgs = []
        p_name = post_data['p_name']
        p_description = post_data['p_description']
        p_category = post_data['p_category']
        new_p_category = post_data['new_p_category']
        p_price = post_data['p_price']
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
        # regex for price
        elif not PRICE_REGEX.match(p_price):
            error_msgs.append('Invalid price')
        if error_msgs:
            return {'errors': error_msgs}
        else:
            # create product
            the_product = Product.productManager.create(name=p_name, description=p_description, image=image, price=p_price)
            # depending on what we return
            return {'the_product': the_product}

#class OrderManager(models.Manager):
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
    #addr_street =   models.CharField(max_length=100)
    #street_two  =   models.CharField(max_length=100)
    #addr_city   =   models.CharField(max_length=100)
    #addr_state  =   models.CharField(max_length=20)
    #addr_zip    =   models.IntegerField()
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    userManager =   UserManager()

class Product(models.Model):
    name        =   models.CharField(max_length=60)
    description =   models.TextField(max_length=1000)
    image       =   models.CharField(max_length=100)
    price       =   models.DecimalField(max_digits=5,decimal_places=2)
    #category    =   models.CharField(max_length=60)
    quantity    =   models.IntegerField(default=0)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    productManager = ProductManager()

class Category(models.Model):
    name        =   models.CharField(max_length=60)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    products    =   models.ManyToManyField(Product, related_name='product_categories')

class Order(models.Model):
    products    =   models.ManyToManyField(Product, related_name="product_orders")
    user        =   models.ForeignKey(User, related_name="user_orders")
    # shipping address
    ####
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

# ============== #
# === STRIPE === #
# ============== #
class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        # bring in stripe, and get the api key from settings.py
        import stripe
        stripe.api_key = "sk_test_5HJSvP0XKmzN122N5ntJ3zfM"

        self.stripe = stripe

    # store the stripe charge id for this sale
    charge_id = models.CharField(max_length=32)

    # you could also store other information about the sale
    # but I'll leave that to you!

    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """

        if self.charge_id: # don't let this be charged twice!
            return False, Exception(message="Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = {
                    "number" : number,
                    "exp_month" : exp_month,
                    "exp_year" : exp_year,
                    "cvc" : cvc,

                    #### it is recommended to include the address!
                    #"address_line1" : self.address1,
                    #"address_line2" : self.address2,
                    #"daddress_zip" : self.zip_code,
                    #"address_state" : self.state,
                },
                description='Thank you for your purchase!')

            self.charge_id = response.id

        except self.stripe.CardError, ce:
            # charge failed
            return False, ce

        return True, response

    def validate_card(request, post_data):
        error_msgs=[]
        if not NO_LET_REGEX.match(post_data['number']):
            error.msgs.append('Card Number invalid')
        if len(post_data['number']) < 16:
            error.msgs.append('Card number invalid')
        if len(post_data['cvc']) != 3:
            error.msgs.append('CVC is invalid')

        if error_msgs:
            return {'errors',error_msgs}
        else:
            return {'validated_card': 'validated'}

# ===================== #
# === END OF STRIPE === #
# ===================== #
