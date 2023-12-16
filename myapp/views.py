
from .models import Category, Product
from django.shortcuts import render, redirect

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

def search_products(request):
    query = request.GET.get('search')
    products = None

    if query:
        products = Product.objects.filter(name__icontains=query)

    return render(request, 'category_detail.html', {'products': products})





def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Получение корзины из сессии или создание новой, если ее нет
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id))

    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart

    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, item_info in cart.items():
        total += item_info['price'] * item_info['quantity']
        cart_items.append({
            'id': item_id,
            'name': item_info['name'],
            'price': item_info['price'],
            'quantity': item_info['quantity'],
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
