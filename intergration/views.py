from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .wazuh.client import get_platform_wazuh_client
from .wazuh.agents import get_agents, get_agents_summary, get_agent_detail
from .wazuh.alerts import get_alerts
from .wazuh.groups import get_enrollment_key, assign_agent_to_tenant


# ── Platform admin ────────────────────────────────────────────────────────────

def wazuh_status(request):
    """Platform-level Wazuh health check."""
    try:
        client  = get_platform_wazuh_client()
        info    = client.get("/")
        summary = client.get("/agents/summary/status")
        return JsonResponse({
            "api_version": info["data"]["api_version"],
            "hostname":    info["data"]["hostname"],
            "agents":      summary["data"],
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ── Tenant views ──────────────────────────────────────────────────────────────

@login_required
def agents_view(request):
    """Main agents page for the tenant."""
    tenant  = request.tenant
    agents  = get_agents(tenant)
    summary = get_agents_summary(tenant)
    enroll  = get_enrollment_key(tenant)

    return render(request, "intergration/agents.html", {
        "agents":  agents,
        "summary": summary,
        "enroll":  enroll,
    })


@login_required
def agent_detail_view(request, agent_id):
    """Single agent detail page."""
    try:
        tenant = request.tenant
        agent  = get_agent_detail(tenant, agent_id)
        alerts = get_alerts(tenant, limit=10)
        alerts = [a for a in alerts if str(a.get("agent", {}).get("id")) == str(agent_id)]

        return render(request, "intergration/agent_detail.html", {
            "agent":  agent,
            "alerts": alerts,
        })
    except PermissionError:
        return JsonResponse({"error": "Agent not found."}, status=404)


@login_required
def assign_agent_view(request):
    """Assign an unassigned agent to this tenant's group."""
    if request.method == "POST":
        agent_id = request.POST.get("agent_id")
        try:
            assign_agent_to_tenant(request.tenant, agent_id)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)


@login_required
def enrollment_instructions_view(request):
    """
    Show the tenant how to install and enroll a Wazuh agent.
    """
    enroll = get_enrollment_key(request.tenant)

    return render(request, "intergration/enroll.html", {
        "enroll": enroll,
    })


# ── API endpoints ─────────────────────────────────────────────────────────────

@login_required
def api_agents(request):
    agents = get_agents(request.tenant)
    return JsonResponse({"agents": agents})


@login_required
def api_alerts(request):
    limit  = int(request.GET.get("limit", 20))
    alerts = get_alerts(request.tenant, limit=limit)
    return JsonResponse({"alerts": alerts})


@login_required
def api_summary(request):
    summary = get_agents_summary(request.tenant)
    return JsonResponse(summary)