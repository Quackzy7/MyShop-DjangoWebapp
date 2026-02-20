from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerProfile, BuyerProfile,Product

class BuyerSignUpForm(UserCreationForm):
    shipping_address = forms.CharField()
    phone_number = forms.CharField()
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'buyer'
        if commit:
            user.save()
            BuyerProfile.objects.create(
                user=user,
                shipping_address=self.cleaned_data['shipping_address'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user
    
class SellerSignUpForm(UserCreationForm):
    shop_name = forms.CharField()
    gst_number = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self,commit=True):
        user=super().save(commit=False)
        user.user_type='seller'
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                shop_name=self.cleaned_data['shop_name'],
                gst_number=self.cleaned_data['gst_number']
            )
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','price','stock','description']