from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from api.models.base import BaseModel
from api.utils.helpers import generate_category_code
class Category(BaseModel,MPTTModel):
    code = models.CharField(unique=True, max_length=100, db_index=True)
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['code']

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.title  

    def save(self,*args,**kwargs):
        if not self.code:
            self.code = generate_category_code()
        super().save(*args,**kwargs)    

    