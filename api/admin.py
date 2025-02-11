from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.accounts import User

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

admin.site.register(User, CustomUserAdmin)