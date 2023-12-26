import os
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import Product, CartItem, OrderItem, Order, Category


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

from django.db.models import F

def create_order(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session=session_key)

    if request.method == 'POST':
        cart_items = CartItem.objects.filter(session=session_key)

        if not cart_items.exists():
            return render(request, 'empty_cart.html')  # Сообщение о пустой корзине

        # Получение данных из формы оформления заказа
        address = request.POST.get('address')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')

        # Вычисление общей суммы заказа и количества товаров
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)

        # Создание заказа
        order = Order.objects.create(
            session_id=session_key,
            address=address,
            total_price=total_price,
            quantity=quantity,
            name=name,
            phone_number=phone_number
        )

        # Уменьшение количества продуктов на складе после оформления заказа
        for cart_item in cart_items:
            product = cart_item.product
            quantity_to_reduce = cart_item.quantity
            product.quantity_available -= quantity_to_reduce  # Предполагается, что у продукта есть поле quantity
            product.save()

            # Или если у вас есть возможность использовать F-объекты для обновления в базе данных без извлечения объекта
            # Примерно так:
            # Product.objects.filter(id=product.id).update(quantity=F('quantity') - quantity_to_reduce)

            # Создание записи OrderItem для каждого элемента корзины
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity
            )

        # Очистка корзины после оформления заказа
        cart_items.delete()

        # Вывод деталей заказа на странице
        return redirect('order_detail', order_id=order.pk)

    return render(request, 'order.html', {'cart_items': cart_items})


def view_all_orders(request):
    orders = Order.objects.all()
    return render(request, 'all_orders.html', {'orders': orders})






def generate_order_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Установка шрифта DejaVuSans, поддерживающего кириллицу
    font_path = os.path.join('DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    pdf.setFont("DejaVuSans", 12)

    pdf.drawString(100, 800, f"Order ID: {order.id}")
    pdf.drawString(100, 780, f"Name: {order.name}")
    pdf.drawString(100, 760, f"Phone Number: {order.phone_number}")
    pdf.drawString(100, 740, f"Address: {order.address}")
    pdf.drawString(100, 720, f"Total Price: {order.total_price}")
    pdf.drawString(100, 700, f"Quantity: {order.quantity}")
    pdf.drawString(100, 680, f"Status: {order.status}")

    formatted_date = order.created_at.strftime('%Y-%m-%d')
    formatted_time = order.created_at.strftime('%H:%M:%S')
    pdf.drawString(100, 660, f"Date: {formatted_date}")
    pdf.drawString(100, 640, f"Time: {formatted_time}")

    y_coordinate = 600  # Начальная координата для отрисовки информации о товарах

    for order_item in order_items:
        total = order_item.quantity * order_item.product.price

        product_name = order_item.product.name
        quantity = order_item.quantity
        price = order_item.product.price

        text = f"{quantity} x {product_name} - {price:.2f} - {total:.2f}"
        pdf.drawString(100, y_coordinate, text)
        y_coordinate -= 20
    image_path = 'media/images/k.png'  # Путь к вашему изображению
    pdf.drawImage(image_path, 350,600, width=220, height=210)
    pdf.showPage()
    pdf.save()

    pdf_data = buffer.getvalue()
    buffer.close()
    response.write(pdf_data)

    return response





def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    items_with_total = []
    for order_item in order_items:
        total = order_item.quantity * order_item.product.price
        items_with_total.append({
            'order_item': order_item,
            'total': total,

        })

    context = {
        'order': order,
        'items_with_total': items_with_total,
    }

    return render(request, 'order_detail.html', context)
