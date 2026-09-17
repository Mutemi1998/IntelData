from django.db import models
from customers.models import Tenant
from django.utils import timezone



class Service(models.Model):
    """
    Platform service catalog
    """
    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    """
    Starter / Professional / Enterprise
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    yearly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    max_users = models.PositiveIntegerField(
        default=5
    )

    max_assets = models.PositiveIntegerField(
        default=100
    )

    max_incidents = models.PositiveIntegerField(
        default=1000
    )

    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name="plans"
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["monthly_price"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Active tenant subscription
    """

    STATUS_CHOICES = [
        ("trial", "Trial"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("suspended", "Suspended"),
        ("cancelled", "Cancelled"),
    ]

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="trial"
    )

    start_date = models.DateField()

    end_date = models.DateField()

    auto_renew = models.BooleanField(
        default=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name}"


class SubscriptionService(models.Model):
    """
    Tenant-specific add-ons
    """

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="addons"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    enabled = models.BooleanField(
        default=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
                )

    class Meta:
        unique_together = (
            "subscription",
            "service"
        )

    def __str__(self):
        return (
            f"{self.subscription.tenant.name}"
            f" - {self.service.name}"
        )
