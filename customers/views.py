from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from accounts.models import TenantUser
from intergration.models import PlatformIntegration
from intergration.models import PlatformIntegration
from intergration.wazuh.groups import get_or_create_tenant_group
from subscriptions.models import Subscription
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as django_settings

from accounts.models import TenantUser           # adjust to your actual import
from subscriptions.views import billing_context        # the helper we just wrote


@login_required
def settings(request):
    # ── Memberships — exclude public tenant ──────────────────────────────────
    memberships = TenantUser.objects.filter(
        user=request.user
    ).select_related("tenant", "user").exclude(
        tenant__schema_name="public"
    )

    membership = memberships.order_by("created_at").first()
    if not membership:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    tenant = membership.tenant
    print(f"Resolved tenant: schema={tenant.schema_name}, name={tenant.name}")

    # ── Team ─────────────────────────────────────────────────────────────────
    all_memberships = (
        TenantUser.objects.filter(tenant=tenant)
        .select_related("user")
        .order_by("created_at")
    )

    user_count  = all_memberships.count()
    asset_count = tenant.assets.count() if hasattr(tenant, "assets") else 0

    # ── Role matrix ──────────────────────────────────────────────────────────
    role_matrix = [
        {"label": "View alerts",             "values": [True,  True,  True,  True,  True]},
        {"label": "Acknowledge alerts",      "values": [True,  True,  True,  False, False]},
        {"label": "Manage users",            "values": [True,  False, False, False, False]},
        {"label": "Configure agents",        "values": [True,  True,  False, False, False]},
        {"label": "Billing / subscription",  "values": [True,  False, False, False, False]},
        {"label": "Run vulnerability scans", "values": [True,  True,  True,  False, False]},
        {"label": "View reports",            "values": [True,  True,  True,  True,  True]},
        {"label": "Manage integrations",     "values": [True,  False, False, False, False]},
    ]

    # ── Wazuh ────────────────────────────────────────────────────────────────
    try:
        integration = PlatformIntegration.objects.get(
            integration_type="wazuh",
            enabled=True,
        )
        wazuh_manager_ip = integration.base_url \
            .replace("https://", "") \
            .replace("http://", "") \
            .split(":")[0]
        wazuh_status = integration.get_status_display()
        wazuh_group  = get_or_create_tenant_group(tenant)
        print(f"Wazuh group resolved: {wazuh_group}")

    except ValueError as e:
        # Caught the public tenant guard
        print(f"[Wazuh] Group error: {e}")
        wazuh_manager_ip = "Not configured"
        wazuh_status     = "Unavailable"
        wazuh_group      = ""

    except PlatformIntegration.DoesNotExist:
        wazuh_manager_ip = "Not configured"
        wazuh_status     = "Unavailable"
        wazuh_group      = ""

    platforms = [
        "X (Twitter)",
        "LinkedIn",
        "Facebook",
        "Instagram",
        "Telegram",
        "WhatsApp",
        "YouTube",
        "TikTok",
    ]

    # ── Context ───────────────────────────────────────────────────────────────
    ctx = {
        "memberships":      memberships,
        "all_memberships":  all_memberships,
        "user_count":       user_count,
        "asset_count":      asset_count,
        "role_matrix":      role_matrix,
        "wazuh_manager_ip": wazuh_manager_ip,
        "wazuh_status":     wazuh_status,
        "wazuh_group":      wazuh_group,
        "platforms": platforms,
    }
    ctx.update(billing_context(request, tenant))

    return render(request, "customers/base.html", ctx)

@login_required
def brand_protection(request):
    membership = TenantUser.objects.filter( user=request.user ).select_related("tenant").exclude( tenant__schema_name="public" ).first()
    if not membership:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return render(request, "customers/brand_protection.html", { "membership": membership, })