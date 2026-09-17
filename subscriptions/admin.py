from django.contrib import admin
from .models import Subscription, SubscriptionPlan

from django.contrib import admin

from .models import (
    Service,
    SubscriptionPlan,
    Subscription,
    SubscriptionService
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "active"
    )

    search_fields = (
        "name",
        "code"
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "monthly_price",
        "max_users",
        "max_assets",
        "active"
    )

    filter_horizontal = (
        "services",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "plan",
        "status",
        "start_date",
        "end_date"
    )

    list_filter = (
        "status",
    )


@admin.register(SubscriptionService)
class SubscriptionServiceAdmin(admin.ModelAdmin):
    list_display = (
        "subscription",
        "service",
        "enabled"
    )