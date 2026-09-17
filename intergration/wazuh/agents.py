from .client import get_platform_wazuh_client
from .groups import get_or_create_tenant_group


def get_agents(tenant):
    group  = get_or_create_tenant_group(tenant)
    client = get_platform_wazuh_client()

    try:
        data = client.get(f"/groups/{group}/agents")
        return data.get("data", {}).get("affected_items", [])
    except Exception:
        return []


def get_agents_summary(tenant):
    """Active, disconnected, never connected counts."""
    agents = get_agents(tenant)
    summary = {
        "total":           len(agents),
        "active":          0,
        "disconnected":    0,
        "never_connected": 0,
        "pending":         0,
    }
    for agent in agents:
        status = agent.get("status", "never_connected")
        if status in summary:
            summary[status] += 1
    return summary


def get_agent_detail(tenant, agent_id):
    """Single agent — must belong to this tenant."""
    agents    = get_agents(tenant)
    agent_ids = {str(a["id"]) for a in agents}

    if str(agent_id) not in agent_ids:
        raise PermissionError(f"Agent {agent_id} does not belong to this tenant.")

    client = get_platform_wazuh_client()
    data   = client.get(f"/agents", params={"agents_list": agent_id})
    return data.get("data", {}).get("affected_items", [{}])[0]


def get_disconnected_agents(tenant):
    agents = get_agents(tenant)
    return [a for a in agents if a.get("status") == "disconnected"]