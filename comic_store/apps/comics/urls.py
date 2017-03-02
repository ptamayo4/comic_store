from django.conf.urls import url, include
from . import views

urlpatterns = [
    # ============== #
    url(r'^test$',views.test),
    url(r'^addtest$',views.add_test),
    # FOR TESTING ONLY
    # ============== #
    url(r'^$', views.index),
    url(r'^admin$', views.admin),
    url(r'^dashboard$', views.admin_login),
    url(r'^register$', views.register),
    url(r'^dashboard/products$', views.product_view),
    url(r'^dashboard/orders$', views.orders_view),
    url(r'^products_main$', views.products_main),
    url(r'^product/category/(?P<category_id>\d+)$',views.product_category),
    url(r'^product_spotlight/(?P<product_id>\d+)$', views.product_spotlight),
    url(r'^shopping_cart$', views.shopping_cart),
    url(r'product_adder$', views.product_adder),
    url(r'^display_test$', views.display_test)
]
