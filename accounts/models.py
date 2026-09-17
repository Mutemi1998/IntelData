from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(
        max_length=30,
        blank=True
    )
    is_platform_admin = models.BooleanField(
        default=False
    )

class TenantUser(models.Model):

    ROLE_CHOICES = [
        ("tenant_admin", "Tenant Admin"),
        ("soc_manager", "SOC Manager"),
        ("soc_analyst", "SOC Analyst"),
        ("tenant_user", "Tenant User"),
        ("readonly", "Read Only"),
    ]

    tenant = models.ForeignKey(
        "customers.Tenant",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "user"],
                name="unique_tenant_user"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.tenant.name} - {self.role}"
