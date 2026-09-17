import logging
from django.utils import timezone
from intergration.models import PlatformIntegration
from .agents import get_agents

logger = logging.getLogger(__name__)


def sync_wazuh_tenant(tenant):
    """
    Sync one tenant's agents from the shared Wazuh instance.
    Run this per tenant via Celery beat later.
    """
    try:
        agents = get_agents(tenant)
        logger.info(f"Wazuh sync OK — {tenant}: {len(agents)} agents")
        return agents

    except Exception as exc:
        integration = PlatformIntegration.objects.filter(
            integration_type="wazuh"
        ).first()

        if integration:
            integration.status     = "error"
            integration.last_error = str(exc)
            integration.save(update_fields=["status", "last_error"])

        logger.error(f"Wazuh sync failed for {tenant}: {exc}")
        raise


def sync_platform_wazuh():
    """
    Called once to verify the platform Wazuh connection is alive.
    """
    from .client import get_platform_wazuh_client
    from django.utils import timezone

    client = get_platform_wazuh_client()
    result = client.get("/")

    PlatformIntegration.objects.filter(
        integration_type="wazuh"
    ).update(
        status     = "active",
        last_sync  = timezone.now(),
        last_error = "",
    )

    return result