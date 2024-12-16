# myapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .permissions import assign_store_manager_permissions

@receiver(post_migrate)
def assign_permissions(sender, **kwargs):
    # Assign the permissions after migrations have been applied
    print("post_migrate signal triggered!")
    assign_store_manager_permissions()
