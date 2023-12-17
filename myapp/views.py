from django.contrib.sessions.models import Session
from .models import Category, Product, CartItem
from django.shortcuts import render, redirect,get_object_or_404

from .models import Product
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def view_cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session=session_key)

    return render(request, 'cart.html', {'cart_items': cart_items})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Значение по умолчанию 1
        session_key = request.session.session_key  # Получаем ключ сессии текущего пользователя

        if session_key:  # Проверяем, есть ли у пользователя ключ сессии
            cart_item, created = CartItem.objects.get_or_create(product=product, session_id=session_key)
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('category_detail', category_id=product.category.id)