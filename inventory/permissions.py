# myapp/permissions.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product

def assign_store_manager_permissions():
    # Get or create the Store Manager group
    group, created = Group.objects.get_or_create(name='Store Manager')

    if created:
        print("Store Manager group created successfully.")
    else:
        print("Store Manager group already exists.")
    # Define the permissions you want to assign
    content_type = ContentType.objects.get_for_model(Product)

    # Permissions for store managers (e.g., change stock and price)
    permission_update_stock = Permission.objects.get(
        content_type=content_type,
        codename='change_stock'
    )
    permission_update_price = Permission.objects.get(
        content_type=content_type,
        codename='change_price'
    )

    # Add permissions to the Store Manager group
    group.permissions.add(permission_update_stock, permission_update_price)
