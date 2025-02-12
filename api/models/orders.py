from api.models.base import BaseModel
from api.models.customers import Customer
from django.db import models

from api.models.products import Product
from api.utils.choices import ORDER_STATUS


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=ORDER_STATUS, default=ORDER_STATUS.pending)

    class Meta:
        ordering = ['-created_at',]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    
    def __str__(self):
        return f"Order {self.id} - {self.customer} ({self.get_status_display()})"    


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ['order', 'product'] 

    def __str__(self):
        return f"{self.order.id} - {self.product.title} x {self.quantity}"    

