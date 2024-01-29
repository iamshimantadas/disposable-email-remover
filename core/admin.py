from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    ordering = (
        "email",
        "id",
    )

    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_manager",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = ("first_name", "last_name", "email")

    list_filter = ("is_staff", "is_active")

    # list_editable = ("is_staff", "is_superuser", "is_active")

    exclude = ("username", "date_joined")

    add_fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Contact Info",
            {
                "fields": ("email","address", ),
            },
        ),
        (
            "Password",
            {
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Contact Info",
            {
                "fields": (
                    "email",
                    "address",
                )
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
                "classes": ["wide", "extrapretty"],
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        ("Password", {"fields": ("password",)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(ValidEmail)
admin.site.register(InvalidEmail)