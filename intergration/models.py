from django.db import models


class PlatformIntegration(models.Model):
    """
    Platform-level integrations — configured once by the platform admin.
    No tenant FK. Tenants never see or touch this.
    """

    TYPE_CHOICES = [
        ("wazuh",      "Wazuh"),
        ("misp",       "MISP"),
        ("openvas",    "OpenVAS"),
        ("virustotal", "VirusTotal"),
    ]

    STATUS_CHOICES = [
        ("pending",  "Pending"),
        ("active",   "Active"),
        ("disabled", "Disabled"),
        ("error",    "Error"),
    ]

    name             = models.CharField(max_length=150)
    integration_type = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    base_url         = models.URLField()
    port             = models.PositiveIntegerField(null=True, blank=True,default=55000)
    status           = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    verify_ssl       = models.BooleanField(default=False)
    enabled          = models.BooleanField(default=True)
    last_sync        = models.DateTimeField(null=True, blank=True)
    last_error       = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_integration_type_display()} — {self.base_url}"


class PlatformIntegrationCredential(models.Model):
    """
    Credentials for the platform-level integration.
    Only one credential per integration (OneToOne).
    """

    integration = models.OneToOneField(
        PlatformIntegration,
        on_delete=models.CASCADE,
        related_name="credential",
    )
    username   = models.CharField(max_length=255, blank=True)
    password   = models.CharField(max_length=255, blank=True)
    token      = models.TextField(blank=True)
    extra      = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credentials → {self.integration}"


class TenantWazuhGroup(models.Model):
    """
    Maps each tenant to their Wazuh group.
    This is how tenant data is isolated inside the shared Wazuh instance.
    """

    tenant     = models.OneToOneField(
        "customers.Tenant",
        on_delete=models.CASCADE,
        related_name="wazuh_group",
    )
    group_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Wazuh group name for this tenant e.g. tenant_acme",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant} → {self.group_name}"