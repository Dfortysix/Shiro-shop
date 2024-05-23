from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem,Cart
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct
from store.models import Product,Variation
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random
import json
import re
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def sendEmail(request, order):
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def place_order(request,total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax if "tax" in locals() else "",
        'grand_total': grand_total if "tax" in locals() else 0,
    }
    return render(request,'orders/checkout.html',context=context)


def order_complete(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        country = request.POST['country']
        city = request.POST['city']
        order_note = request.POST['order_note']
        order_total = request.GET.get('grand_total')
        tax = request.GET.get('tax')
        # Tạo QuerySet từ danh sách các CartItem object
        # Lấy thông tin người dùng từ session
        user = request.user

        today = datetime.datetime.today()
        random_number = random.randint(100000, 999999)
        order_number = f"ORD-{today.year}{today.month}{today.day}{today.minute}{today.second}-{user.id}-{_cart_id(request)}"
        # Tạo đơn hàng mới
        is_exists_order = Order.objects.filter(order_number=order_number).exists()
        if is_exists_order == False:
            order = Order.objects.create(
                user=user,
                order_number = order_number,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                country=country,
                city=city,
                order_note=order_note,
                order_total=order_total,
                status="Completed",
                tax=tax,
                is_ordered=True
            )
        else:
            order = {}



        # Lưu đơn hàng
            order.save()

        #Lay ra product and variation
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except ObjectDoesNotExist:
            pass  # Chỉ bỏ qua
        products_list = []
        for cart_item in cart_items:
            product_name = cart_item.product.product_name
            products_list.append(product_name)
        products = Product.objects.filter(product_name__in=products_list)
        print(products)
        for product in products:
            cart_items = CartItem.objects.filter(user=user,product=product)
            print(f"cartsitem : {cart_items}")
            variations = [list(item.variations.all()) for item in cart_items]
            print(f"variation: {variations}")
            count = 0
            for variation in variations:
                print(variation)
                for var in variation:
                    variation_category = var.variation_category
                    variation_value = var.variation_value
                    quantity = [item.quantity for item in cart_items][count]
                    variation_object = Variation.objects.get(product=product,
                                                             variation_category__iexact=variation_category,
                                                             variation_value__iexact=variation_value)
                    order_product = OrderProduct.objects.create(
                        order=order,
                        user=user,
                        product=product,
                        quantity= quantity,
                        product_price = product.price,
                        ordered = True,

                    )
                    order_product.variations.add(variation_object)
                    order_product.save()

                count +=1
                print(quantity)
            #variation = Variation.objects.filter()




        context ={
            'order_number': order_number,
        }
        # Chuyển hướng đến trang xác nhận đơn hàng
        return render(request,'orders/order_complete.html',context=context)
    else:
        return render(request, 'your_template.html')
