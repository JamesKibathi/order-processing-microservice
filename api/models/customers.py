from api.models.base import BaseModel
from django.db import models


class Customer(BaseModel):
    name =  models.CharField(max_length=256)
    phonenumber = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=256)


    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created_at',]