import re
from django import forms
from .models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category']

    # Custom validation for name to ensure only letters and spaces
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Check if the name is not empty
        if not name or len(name) < 1:
            raise forms.ValidationError('Name is required')

        # Check if the name contains only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')

        return name



class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category']

    # Reusing the same validations from the create form
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Check if the name is not empty
        if not name or len(name) < 1:
            raise forms.ValidationError('Name is required')

        # Check if the name contains only letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Name must contain only letters and spaces')

        return name
