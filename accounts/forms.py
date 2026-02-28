from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BuyerProfile, SellerProfile

TW = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 transition-colors bg-white'

class BuyerSignUpForm(UserCreationForm):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': TW, 'rows': 2})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': TW}),
            'email': forms.EmailInput(attrs={'class': TW}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': TW})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': TW})

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
    shop_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW})
    )
    gst_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': TW}),
            'email': forms.EmailInput(attrs={'class': TW}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': TW})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': TW})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seller'
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                shop_name=self.cleaned_data['shop_name'],
                gst_number=self.cleaned_data['gst_number']
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': TW, 'placeholder': 'Password'})
    )