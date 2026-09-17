from django.contrib import admin
from .models import User, TenantUser
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "IntelData",
            {
                "fields": (
                    "phone",
                    "is_platform_admin",
                )
            }
        ),
    )


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "tenant",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
        "tenant",
    )

    search_fields = (
        "user__username",
        "user__email",
        "tenant__name",
    )
