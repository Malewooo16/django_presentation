from django.db import models
from django.contrib.auth.models import User
from inventory.models import StoreProduct

class Dispatch(models.Model):
    store_product = models.ForeignKey(
        StoreProduct, related_name="dispatches", on_delete=models.CASCADE
    )
    quantity_sold = models.PositiveIntegerField()
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, blank=True, null=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override save method to calculate the total amount dynamically.
        Total = (Price * Quantity) - Discount
        """
        self.total_amount = (self.store_product.price * self.quantity_sold) - (
            self.discount or 0
        )
        super(Dispatch, self).save(*args, **kwargs)

    def __str__(self):
        return f"Dispatch: {self.quantity_sold} x {self.store_product.product.name} at {self.store_product.store.name}"
