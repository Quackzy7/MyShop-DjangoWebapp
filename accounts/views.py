from django.shortcuts import render,redirect
from .forms import BuyerSignUpForm, SellerSignUpForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# Create your views here.

def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailBackend')
            return redirect('products')
    else:
        form = BuyerSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'type': 'Buyer'})

def seller_signup(request):

    if request.method=="POST":
        form=SellerSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user, backend='accounts.backends.EmailBackend')
            return redirect('seller_dashboard')
    else:
        form=SellerSignUpForm()
    return render(request,'accounts/signup.html',{'form':form,'type':'Seller'})    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
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

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('products')   


