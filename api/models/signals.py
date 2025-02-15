import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.utils.services import EmailService, SendSMS
from .orders import Order
@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    """Send SMS to customer and email to admin when an order is placed."""
    if created:
        send_order_sms(instance)
        send_admin_email(instance)
        print("Signal Triggered...")

def send_order_sms(order):
    """Send an SMS to the customer about their order placement."""
    customer_phone = order.customer.phonenumber 
    message = f"Dear {order.customer.name}, your order #{order.order_number} has been placed successfully. Total: Ksh{order.total_amount}. Thank you!"
    
    sms_service = SendSMS()
    response = sms_service.send(message, [customer_phone])
    
def send_admin_email(order):
    """Send an email to the administrator about the new order."""
    admin_email = settings.ADMIN_EMAIL 
    subject = f"New Order Placed - {order.order_number}"
    message = f"""
    A new order has been placed.
    
    Order ID: {order.order_number}
    Customer: {order.customer.name}
    Total Amount: ksh.{order.total_amount}
    Order Status: {order.status}
    """
    
    email_service = EmailService()
    response = email_service.send_email(subject, message, [admin_email])
  

