from django.urls import path
from . import views

urlpatterns = [
    # Platform
    path("status/",              views.wazuh_status,               name="wazuh-status"),

    # Tenant pages
    path("agents/",              views.agents_view,                 name="wazuh-agents"),
    path("agents/<str:agent_id>/", views.agent_detail_view,         name="wazuh-agent-detail"),
    path("agents/assign/",       views.assign_agent_view,           name="wazuh-assign-agent"),
    path("enroll/",              views.enrollment_instructions_view, name="wazuh-enroll"),

    # JSON API
    path("api/agents/",          views.api_agents,                  name="api-agents"),
    path("api/alerts/",          views.api_alerts,                  name="api-alerts"),
    path("api/summary/",         views.api_summary,                 name="api-summary"),
]