from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Category, Product, Store, StoreProduct
from inventory.forms import ProductUpdateForm


# Custom Mixin to restrict access to superusers
class SuperUserRequiredMixin(AccessMixin):
    """
    Mixin to restrict access to superusers. 
    Redirects unauthorized users to login page or another specified URL.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect unauthenticated users to login page
            return redirect('/store/login')  # Change 'login' to your login URL name
        
        if not request.user.is_superuser:
            # Redirect non-superusers to a custom page, like 'home'
            return redirect('/store/login')  # Change 'home' to the URL name you want
        
        # If user is authenticated and is superuser, proceed to the view
        return super().dispatch(request, *args, **kwargs)


# Home page view
class HomeView(SuperUserRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'


# Category views
class CategoryListView(SuperUserRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(SuperUserRequiredMixin, CreateView):
    model = Category
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Category
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')


# Product views
class ProductListView(SuperUserRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'


class ProductCreateView(SuperUserRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'description']
    template_name = 'inventory/product_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # After the product is created, add it to all stores
        product = self.object
        stores = Store.objects.all()

        for store in stores:
            StoreProduct.objects.create(
                store=store,
                product=product,
                price=10.00,  # Default price
                quantity=100,  # Default quantity
            )

        messages.success(self.request, "Product created successfully and added to all stores.")
        return redirect('product-list')

    def get_success_url(self):
        return reverse_lazy('product-list')


class ProductUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'inventory/product_update.html'
    context_object_name = 'product'

    def form_valid(self, form):
        product = form.save(commit=False)
        if 'name' in form.changed_data:
            product.name = form.cleaned_data['name']
        product.save()
        return redirect('product-list')


class ProductDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_delete.html'
    success_url = reverse_lazy('product-list')
