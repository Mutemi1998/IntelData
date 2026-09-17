from django.utils import timezone
from .client import get_platform_wazuh_client
from intergration.models import TenantWazuhGroup, PlatformIntegration


def get_or_create_tenant_group(tenant):
    # Guard against public tenant
    if tenant.schema_name == "public":
        raise ValueError(
            f"Cannot create Wazuh group for public tenant. "
            f"Check your membership query."
        )

    group_name = f"{tenant.schema_name}"

    obj, created = TenantWazuhGroup.objects.get_or_create(
        tenant   = tenant,
        defaults = {"group_name": group_name},
    )

    if created:
        _create_wazuh_group(group_name)
    else:
        _ensure_wazuh_group(group_name)

    # Mark integration active now that it is working
    PlatformIntegration.objects.filter(
        integration_type = "wazuh",
        enabled          = True,
    ).update(
        status    = "active",
        last_sync = timezone.now(),
    )

    return obj.group_name


def _create_wazuh_group(group_name):
    try:
        client = get_platform_wazuh_client()
        client.post("/groups", json={"group_id": group_name})
        print(f"[Wazuh] Created group: {group_name}")
    except Exception as e:
        if "already exists" not in str(e).lower():
            raise


def _ensure_wazuh_group(group_name):
    """Create the group in Wazuh if it was deleted manually."""
    try:
        client = get_platform_wazuh_client()
        groups = client.get("/groups").get("data", {}).get("affected_items", [])
        names  = [g["name"] for g in groups]
        if group_name not in names:
            _create_wazuh_group(group_name)
            print(f"[Wazuh] Re-created missing group: {group_name}")
    except Exception as e:
        print(f"[Wazuh] Could not verify group: {e}")


def get_enrollment_key(tenant):
    """
    Returns the info a tenant needs to enroll agents into their group.
    """
    group_name = get_or_create_tenant_group(tenant)
    client     = get_platform_wazuh_client()

    return {
        "group":      group_name,
        "wazuh_host": client.base_url.replace("https://", "").split(":")[0],
        "wazuh_port": 1514,
        "reg_port":   1515,
    }


def assign_agent_to_tenant(tenant, agent_id):
    """Move an agent into this tenant's Wazuh group."""
    group_name = get_or_create_tenant_group(tenant)
    client     = get_platform_wazuh_client()
    client.put(f"/agents/{agent_id}/group/{group_name}")