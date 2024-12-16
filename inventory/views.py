
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from inventory.forms import ProductUpdateForm
from .models import Category, Product
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

class ProductCreateView(CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    fields = ['name', 'category', 'price', 'description', 'quantity']  # Replace with your Product model fields
    success_url = reverse_lazy('product-list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'inventory/product_update.html'
    context_object_name = 'product'

    def get_object(self):
        # Only allow access to products within the store of the logged-in user
        product = super().get_object()
        store = product.store
        if self.request.user != store.owner:
            # Check if the user is a store manager for this store
            if not self.request.user.groups.filter(name='Store Manager', store=store).exists():
                raise PermissionDenied("You do not have permission to edit this product.")
        return product

    def form_valid(self, form):
        # Only update stock and price, not category
        product = form.save(commit=False)
        if 'stock_quantity' in form.changed_data:
            product.stock_quantity = form.cleaned_data['stock_quantity']
        if 'price' in form.changed_data:
            product.price = form.cleaned_data['price']
        product.save()
        return redirect('product-list')
    

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')