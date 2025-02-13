import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .orders import Order
@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    """Send SMS to customer and email to admin when an order is placed."""
    if created:
        # send_order_sms(instance)
        # send_admin_email(instance)
        print("Signal Triggered")
