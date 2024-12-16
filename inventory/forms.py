# inventory/forms.py
import re
from django import forms
from .models import Product

class ProductCreateForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    category = forms.CharField(max_length=255, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = forms.IntegerField(required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if the name is not empty
        if not name or len(name) < 1:
            raise forms.ValidationError('Name is required')
        
        # Check if the name contains only letters and spaces using a regular expression
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')
        
        return name

    # Custom validation for price to ensure it is positive
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be a positive value.')
        return price

    # Custom validation for stock to ensure it is non-negative
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return quantity

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity']
    
    #Custom validation for name to ensure characters only
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if the name is not empty
        if not name or len(name) < 1:
            raise forms.ValidationError('Name is required')
        
        # Check if the name contains only letters and spaces using a regular expression
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')
        
        return name
    # Custom validation for price to ensure it is positive
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be a positive value.')
        return price

    # Custom validation for stock to ensure it is non-negative
    def clean_stock(self):
        quantity = self.cleaned_data.get('stock')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return quantity