from django import forms
from .models import Product
TW = 'w-full px-3 py-2 text-sm rounded-xl outline-none transition-colors' + \
     ' border border-orange-200 bg-orange-50 text-amber-900' + \
     ' focus:border-orange-400 focus:ring-1 focus:ring-orange-300' + \
     ' placeholder-orange-300'
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': TW, 'placeholder': 'Product name'}),
            'price': forms.NumberInput(attrs={'class': TW, 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': TW, 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': TW, 'rows': 4, 'placeholder': 'Describe your product...'}),
            'category': forms.Select(attrs={'class': TW}),
        }