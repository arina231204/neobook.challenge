from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders/', views.view_all_orders, name='all_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/pdf/', views.generate_order_pdf, name='order_pdf'),






]