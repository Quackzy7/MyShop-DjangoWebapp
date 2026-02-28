from django.shortcuts import render,get_object_or_404,redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Order, OrderItem,Payment
from cart.models import Cart
from .services import create_stripe_payment,confirm_stripe_payment
from django.conf import settings
from accounts.models import BuyerProfile
# Create your views here.
@login_required(login_url='login')
@transaction.atomic
def checkout(request):
    cart=get_object_or_404(Cart,user=request.user)
    if not cart.items.exists():
        return redirect("cart_detail")
    buyer_profile = BuyerProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        shipping_address = request.POST.get("shipping_address", "").strip()
        if buyer_profile:
            buyer_profile.shipping_address = shipping_address
            buyer_profile.save()
        else:
            buyer_profile = BuyerProfile.objects.create(
                user=request.user,
                shipping_address=shipping_address
            )
        order = Order.objects.create(
        user=request.user,
        )
        total=0
        for item in cart.items.all():

            OrderItem.objects.create(   
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                seller=item.product.seller
            )

            item.product.stock -= item.quantity
            item.product.save()

            total+=item.product.price*item.quantity

        order.total_price=total
        order.save()
        cart.items.all().delete()

    
        if payment_method == "stripe":
            client_secret = create_stripe_payment(order)
            return render(request, "orders/stripe_checkout.html", {
            "client_secret": client_secret,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "order": order
            })
        if payment_method=="cod":
            Payment.objects.create(
            order=order,
            payment_method="cod",
            amount=order.total_price,
            status="pending"
            )
            return redirect("order_detail", order_id=order.id)
    return render(request, "orders/checkout.html", {
        "buyer_profile": buyer_profile
    })

@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})

@login_required(login_url='login')
def seller_order_items(request):

    if not request.user.is_seller():
        return HttpResponseForbidden("Only Sellers can access this page !")

    items = OrderItem.objects.filter(
        seller=request.user
    ).order_by("-order__created_at")

    return render(request, "orders/seller_order_items.html", {
        "items": items
    })

@login_required(login_url='login')
def update_order_item(request, item_id):

    item = get_object_or_404(OrderItem, id=item_id)

    if item.seller != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        new_status = request.POST.get("status")
        item.status = new_status
        item.save()

        return redirect("seller_order_items")

    return render(request, "orders/update_item.html", {
        "item": item
    })

@login_required(login_url='login')
def stripe_success(request):
    payment_intent = request.GET.get("payment_intent")

    order = confirm_stripe_payment(payment_intent)

    return redirect("order_detail", order_id=order.id)