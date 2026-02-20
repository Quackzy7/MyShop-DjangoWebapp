from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product
from django.contrib.auth import login,authenticate,logout
from .forms import BuyerSignUpForm, SellerSignUpForm,LoginForm,ProductForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# Create your views here.

def display_products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'store/products.html',context)

def product_detail(request,slug,id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})
    
def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = BuyerSignUpForm()
    return render(request, 'store/signup.html', {'form': form, 'type': 'Buyer'})

def seller_signup(request):

    if request.method=="POST":
        form=SellerSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('/products')
    else:
        form=SellerSignUpForm()
    return render(request,'store/signup.html',{'form':form,'type':'Seller'})    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_seller():
                    return redirect('seller_dashboard')
                else:
                    return redirect('products')
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()

    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('products')   

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
            return redirect('seller_dashboard')
    else:
        form=ProductForm(instance=product)
    return render(request,'store/product_form.html',{'form':form})

        
