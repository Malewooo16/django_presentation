from django import forms
from inventory.models import StoreProduct
from .models import Dispatch

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = StoreProduct
        fields = ['price', 'quantity']

    # Custom validation for stock to ensure it's non-negative
    def clean_stock(self):
        stock = self.cleaned_data.get('quantity')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = ["store_product", "quantity_sold", "discount"]
