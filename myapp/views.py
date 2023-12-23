from django.contrib.sessions.models import Session
from .models import Category, Product, CartItem
from django.shortcuts import render, redirect,get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Product

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

    # Вычисляем общую стоимость для каждого элемента корзины и общую сумму всех товаров
    total_price = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total_price += item.total_price
    all_price = total_price
    # Добавляем стоимость доставки
    delivery_cost = 150
    total_price += delivery_cost

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'all_price': all_price})




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

def delete_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')



def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        # Проверка доступного количества на складе
        if quantity <= cart_item.product.quantity_available:
            cart_item.quantity = quantity
        else:
            cart_item.quantity = cart_item.product.quantity_available

        cart_item.save()

    return redirect('view_cart')


from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                address=form.cleaned_data['address'],
                total_price=form.cleaned_data['total_price'],
                quantity=form.cleaned_data['quantity'],
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number']
            )
            order.save()
            return redirect('success')  # Перенаправление на страницу "успешного оформления заказа"
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form})
