from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from inventory.models import Product, Store, StoreProduct
from django.contrib import messages
from store_management.forms import ProductUpdateForm

# Utility functions for role-based access
def is_admin(user):
    return user.is_superuser

def is_store_manager(user):
    return user.groups.filter(name="Store Manager").exists()

# Authentication Views
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if is_admin(user):
                return redirect("admin_dashboard")
            elif is_store_manager(user):
                return redirect("store_manager_dashboard")
            else:
                messages.error(request, "Access denied. Please contact admin.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "store_management/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    stores = Store.objects.all()
    return render(request, "store_management/admin_dashboard.html", {"stores": stores})

# Store Manager Views
@login_required
@user_passes_test(is_store_manager)
def store_manager_dashboard(request):
    store = request.user.stores.first()  # Fetch the first store the user manages
    if store is None:
        # If the user does not have a store assigned, handle accordingly
        return render(request, "store_management/store_manager_dashboard.html", {
            "error": "You are not managing any store at the moment."
        })

    # Fetch products for the store using StoreProduct model
    store_products = store.store_products.all()  # Get all StoreProduct instances for this store
    products = [store_product.product for store_product in store_products]  # Extract the actual products

    return render(request, "store_management/store_manager_dashboard.html", {
        "store": store,
        "products": products,
    })

@login_required
@user_passes_test(is_store_manager)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the user has permission to update the product in their store
    store_product = StoreProduct.objects.filter(product=product, store__owner=request.user).first()

    if not store_product:
        messages.error(request, "You don't have permission to update this product.")
        return redirect("store_manager_dashboard")

    if request.method == "POST":
        form = ProductUpdateForm(request.POST, instance=store_product)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("store_manager_dashboard")
        else:
            messages.error(request, "There was an error updating the product.")
    else:
        form = ProductUpdateForm(instance=store_product)
    
    return render(request, "store_management/update_product.html", {
        "product": product,
        "form": form,
    })
