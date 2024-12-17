from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from inventory.models import Product, Store, StoreProduct
from django.contrib import messages
from store_management.forms import DispatchForm, ProductUpdateForm
from store_management.models import Dispatch


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

@login_required
@user_passes_test(is_store_manager)
def record_dispatch(request):
    store = request.user.stores.first()

    if request.method == "POST":
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatch = form.save(commit=False)

            # Ensure the product belongs to the store
            if dispatch.store_product.store != store:
                messages.error(request, "You cannot record a dispatch for this product.")
                return redirect("record_dispatch")

            # Check if there is enough stock
            if dispatch.quantity_sold > dispatch.store_product.quantity:
                messages.error(request, "Not enough stock available.")
                return redirect("record_dispatch")

            # Deduct the stock and save
            dispatch.store_product.quantity -= dispatch.quantity_sold
            dispatch.store_product.save()
            dispatch.sold_by = request.user
            dispatch.save()

            messages.success(request, "Dispatch recorded successfully!")
            return redirect("store_manager_dashboard")
    else:
        # Limit products in the form to the store the manager is associated with
        form = DispatchForm()
        form.fields["store_product"].queryset = StoreProduct.objects.filter(store=store)

    return render(
        request,
        "store_management/record_dispatch.html",
        {"form": form},
    )

@login_required
@user_passes_test(is_store_manager)
def dispatch_report(request):
    # Get the store the current store manager manages
    store = request.user.stores.first()
    if not store:
        return render(request, "store_management/dispatch_report.html", {
            "error": "You are not assigned to any store."
        })

    # Retrieve all dispatches related to the store
    dispatches = Dispatch.objects.filter(store_product__store=store)

    # Filter by date range if specified
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date and end_date:
        dispatches = dispatches.filter(timestamp__date__range=[start_date, end_date])

    # Calculate totals
    total_quantity = dispatches.aggregate(Sum("quantity_sold"))["quantity_sold__sum"] or 0
    total_revenue = sum(d.total_amount for d in dispatches)

    context = {
        "store": store,
        "dispatches": dispatches,
        "total_quantity": total_quantity,
        "total_revenue": total_revenue,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "store_management/dispatch_report.html", context)