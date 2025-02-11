from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.accounts import User
from api.models.categories import Category
from api.models.customers import Customer
from api.models.orders import Order
from api.models.products import Product

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "username", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "first_name", "last_name", "phone"),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title','parent')
    ordering = ('parent',)    

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product)
admin.site.register(Order)