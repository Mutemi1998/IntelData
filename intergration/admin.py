from django.contrib import admin
from .models import PlatformIntegration, PlatformIntegrationCredential, TenantWazuhGroup


class CredentialInline(admin.StackedInline):
    model  = PlatformIntegrationCredential
    extra  = 1
    fields = ("username", "password", "token")


@admin.register(PlatformIntegration)
class PlatformIntegrationAdmin(admin.ModelAdmin):
    list_display  = ("name", "integration_type", "base_url", "status", "enabled", "last_sync")
    list_filter   = ("integration_type", "status", "enabled")
    inlines       = [CredentialInline]


@admin.register(TenantWazuhGroup)
class TenantWazuhGroupAdmin(admin.ModelAdmin):
    list_display = ("tenant", "group_name", "created_at")