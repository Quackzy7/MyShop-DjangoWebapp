from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BuyerProfile, SellerProfile

TW = 'w-full px-3 py-2 text-sm rounded-xl outline-none transition-colors' + \
     ' border border-orange-200 bg-orange-50 text-amber-900' + \
     ' focus:border-orange-400 focus:ring-1 focus:ring-orange-300' + \
     ' placeholder-orange-300'


class BuyerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'Last name'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'e.g. 9800000000'})
    )
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': TW, 'rows': 2, 'placeholder': 'Street, City, State, PIN'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': TW, 'placeholder': '@handle'}),
            'email': forms.EmailInput(attrs={'class': TW, 'placeholder': 'you@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': TW})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': TW})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'buyer'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            BuyerProfile.objects.create(
                user=user,
                shipping_address=self.cleaned_data['shipping_address']
            )
        return user


class SellerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'Last name'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW, 'placeholder': 'e.g. 9800000000'})
    )
    shop_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW})
    )
    gst_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': TW})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': TW, 'placeholder': '@handle'}),
            'email': forms.EmailInput(attrs={'class': TW, 'placeholder': 'you@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': TW})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': TW})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seller'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                shop_name=self.cleaned_data['shop_name'],
                gst_number=self.cleaned_data['gst_number']
            )
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': TW, 'placeholder': 'you@example.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': TW, 'placeholder': 'Password'})
    )