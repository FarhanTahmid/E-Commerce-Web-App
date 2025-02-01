from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItems

@receiver([post_save, post_delete], sender=CartItems)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart_id
    total = sum(
        item.quantity * item.product_sku.product_price
        for item in cart.cartitems_set.all()
    )
    cart.cart_total_amount = total
    cart.save()