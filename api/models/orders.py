from api.models.base import BaseModel
from api.models.customers import Customer
from django.db import models

from api.utils.choices import ORDER_STATUS


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=ORDER_STATUS, default=ORDER_STATUS.pending)

    def __str__(self):
        return f"Order {self.customer.name} - {self.status}"
  
    class Meta:
        ordering = ['-created_at',]

