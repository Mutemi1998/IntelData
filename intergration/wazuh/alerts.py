from .client import get_platform_wazuh_client
from .agents import get_agents


def get_alerts(tenant, limit=20, offset=0):
    """
    Get alerts for agents that belong to this tenant.
    Wazuh alerts API filters by agent ID list.
    """
    agents    = get_agents(tenant)
    agent_ids = [str(a["id"]) for a in agents]

    if not agent_ids:
        return []

    client = get_platform_wazuh_client()

    try:
        data = client.get(
            "/alerts",
            params={
                "agents_list": ",".join(agent_ids),
                "limit":       limit,
                "offset":      offset,
                "sort":        "-timestamp",
            },
        )
        return data.get("data", {}).get("affected_items", [])
    except Exception:
        return []