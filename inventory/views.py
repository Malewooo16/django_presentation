
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from inventory.forms import ProductCreateForm, ProductUpdateForm
from .models import Category, Product, Store
from django.core.exceptions import PermissionDenied

# Home page view
class HomeView(TemplateView):
    template_name = 'inventory/home.html'

# Category views
class CategoryListView(ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']  # Replace with your Category model fields
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')

# Product views
class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product, StoreProduct, Store

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'description']
    template_name = 'inventory/product_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # After the product is created, we need to create StoreProduct instances for all stores
        product = self.object  # This is the product just created

        # Fetch all stores
        stores = Store.objects.all()

        for store in stores:
            # Create a StoreProduct instance for each store, with default price and quantity
            StoreProduct.objects.create(
                store=store,
                product=product,
                price=10.00,  # Default price (you can modify this)
                quantity=100,  # Default quantity (you can modify this)
            )

        messages.success(self.request, "Product created successfully and added to all stores.")
        return redirect('product-list')  # Redirect to a success page or wherever you need

    def get_success_url(self):
        return reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'inventory/product_update.html'
    context_object_name = 'product'

    def get_object(self):
        # Only allow access to products within the store of the logged-in user
        product = super().get_object()
        stores = product.stores
       
        return product

    def form_valid(self, form):
        # Only update stock and price, not category
        product = form.save(commit=False)
        if 'name' in form.changed_data:
            product.name = form.cleaned_data['name']
        product.save()
        return redirect('product-list')
    

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/product_delete.html'
    success_url = reverse_lazy('product-list')