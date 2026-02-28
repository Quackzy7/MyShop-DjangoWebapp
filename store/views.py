from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product,ProductImage,Category
from .forms import ProductForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def home(request):
    products = Product.objects.all()[:6]  # Show only 6 featured products
    return render(request, "store/home.html", {"products": products})

def display_products(request):
    query=request.GET.get("q")
    category_slug=request.GET.get("category")

    products=Product.objects.all()
    categories=Category.objects.all()
    if query:
        products=products.filter(Q(name__icontains=query)|Q(description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    context={'products':products,'query':query,'categories':categories}
    return render(request,'store/products.html',context)

def product_detail(request,slug,id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})
    
@login_required(login_url='login')
def seller_dashboard(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("You are not a seller")

    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/seller_dashboard.html', {'products': products})

@login_required(login_url='login')
def add_product(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("You are not a seller")
    
    if request.method=="POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            product=form.save(commit=False)
            product.seller=request.user
            product.save()
            
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product,image=image)
            return redirect("seller_dashboard")
    else:
        form=ProductForm()
    return render(request,'store/product_form.html',{'form':form})

@login_required(login_url='login')
def delete_product(request,id):
    product = get_object_or_404(Product, id=id)
    if product.seller != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'store/confirm_delete.html', {'product': product})

@login_required(login_url='login')
def update_product(request,id):
    product=get_object_or_404(Product,id=id)
    if product.seller != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method=="POST":
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(
                    product=product,
                    image=image
                )
            return redirect('seller_dashboard')
    else:
        form=ProductForm(instance=product)
    return render(request,'store/product_form.html',{'form':form,"product": product})

        
