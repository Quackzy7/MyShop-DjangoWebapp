from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem
from store.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def add_to_cart(request,id):
    product=get_object_or_404(Product,id=id)
    qty=int(request.POST.get('quantity',1))
    if qty < 1:
        qty = 1
    if qty > product.stock:
        qty = product.stock

    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={"quantity":qty})
    if not created:
        cart_item.quantity += qty
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
        cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login')
def cart_detail(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    context={'cart':cart}
    return render(request,'cart/cart.html',context)
    
@login_required(login_url='login')
def remove_from_cart(request,id):
    cart_item=get_object_or_404(CartItem,id=id,cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')