from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import (
    Service,
    Subscription,
    SubscriptionPlan,
    SubscriptionService,
)
from accounts.models import TenantUser


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def is_tenant_admin(user, tenant):
    return TenantUser.objects.filter(
        user=user,
        tenant=tenant,
        role="tenant_admin",
    ).exists()


# ─────────────────────────────────────────────
# Plan list  (public catalogue, no tenant ctx)
# ─────────────────────────────────────────────

@login_required
def plan_list(request):
    """Available plans — standalone page."""
    plans = SubscriptionPlan.objects.filter(active=True).prefetch_related("services")
    return render(request, "subscriptions/plan_list.html", {"plans": plans})


# ─────────────────────────────────────────────
# Current subscription  (standalone page)
# ─────────────────────────────────────────────

@login_required
def current_subscription(request):
    """Show the tenant's current subscription — standalone page."""
    tenant = request.tenant

    subscription = get_object_or_404(Subscription, tenant=tenant)

    addons = SubscriptionService.objects.filter(
        subscription=subscription,
        enabled=True,
    ).select_related("service")

    return render(
        request,
        "subscriptions/current_subscription.html",
        {
            "subscription": subscription,
            "addons":       addons,
        },
    )


# ─────────────────────────────────────────────
# Upgrade / change plan
# ─────────────────────────────────────────────

@login_required
def upgrade_subscription(request, plan_id):
    tenant = request.tenant

    if not is_tenant_admin(request.user, tenant):
        messages.error(request, "Only tenant admins can change the subscription plan.")
        return redirect("settings")          # ← was "current_subscription"

    subscription = get_object_or_404(Subscription, tenant=tenant)
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id, active=True)

    old_plan = subscription.plan
    subscription.plan = plan
    subscription.status = "active"
    subscription.save()

    if plan.monthly_price > old_plan.monthly_price:
        print(f"Upgraded from {old_plan.name} to {plan.name}.")
        messages.success(request, f"Plan upgraded to {plan.name}.")
    elif plan.monthly_price < old_plan.monthly_price:
        print(f"Downgraded from {old_plan.name} to {plan.name}.")
        messages.warning(request, f"Plan downgraded to {plan.name}.")
    else:
        print(f"Switched from {old_plan.name} to {plan.name}.")
        messages.success(request, f"Switched to {plan.name}.")

    return redirect("settings") 

# ─────────────────────────────────────────────
# Service catalogue
# ─────────────────────────────────────────────

@login_required
def service_catalog(request):
    """Standalone service catalogue page."""
    services = Service.objects.filter(active=True)
    return render(
        request,
        "subscriptions/service_catalog.html",
        {"services": services},
    )


# ─────────────────────────────────────────────
# Add / remove add-on services
# ─────────────────────────────────────────────

@login_required
def add_service(request, service_id):
    tenant = request.tenant

    if not is_tenant_admin(request.user, tenant):
        messages.error(request, "Only tenant admins can add services.")
        return redirect("settings")          # ← was "service_catalog"

    subscription = get_object_or_404(Subscription, tenant=tenant)
    service = get_object_or_404(Service, pk=service_id, active=True)

    _, created = SubscriptionService.objects.get_or_create(
        subscription=subscription,
        service=service,
        defaults={"enabled": True},
    )

    if created:
        messages.success(request, f"{service.name} added to your subscription.")
    else:
        messages.info(request, f"{service.name} is already active.")

    return redirect("settings")


@login_required
def remove_service(request, service_id):
    tenant = request.tenant

    if not is_tenant_admin(request.user, tenant):
        messages.error(request, "Only tenant admins can remove services.")
        return redirect("settings")

    subscription = get_object_or_404(Subscription, tenant=tenant)

    deleted, _ = SubscriptionService.objects.filter(
        subscription=subscription,
        service_id=service_id,
    ).delete()

    if deleted:
        messages.success(request, "Service removed.")
    else:
        messages.warning(request, "Service not found on your subscription.")

    return redirect("settings")


# ─────────────────────────────────────────────
# Context helper  (called from customers/views.py → settings view)
# ─────────────────────────────────────────────

def billing_context(request, tenant):
    """
    Return all billing-related context variables needed by the
    sec-billing section in customers/settings.html.

    Usage in customers/views.py::settings():
        from subscriptions.views import billing_context
        ctx.update(billing_context(request, tenant))
    """
    try:
        subscription = Subscription.objects.select_related(
            "plan"
        ).prefetch_related(
            "plan__services"
        ).get(tenant=tenant)
    except Subscription.DoesNotExist:
        subscription = None

    # Add-ons already active for this tenant
    if subscription:
        addons = SubscriptionService.objects.filter(
            subscription=subscription,
            enabled=True,
        ).select_related("service")
        active_addon_ids = set(addons.values_list("service_id", flat=True))
    else:
        addons = SubscriptionService.objects.none()
        active_addon_ids = set()

    # Services that exist but are NOT bundled in the current plan
    # (shown in the "Add-on services" catalogue card)
    if subscription:
        plan_service_ids = set(
            subscription.plan.services.values_list("pk", flat=True)
        )
    else:
        plan_service_ids = set()

    available_services = Service.objects.filter(active=True).exclude(
        pk__in=plan_service_ids
    )

    # All plans for the plan-selector grid
    plans = SubscriptionPlan.objects.filter(
        active=True
    ).prefetch_related("services").order_by("monthly_price")

    # Usage counts  (asset_count and user_count come from the outer settings view,
    # but we include safe defaults here in case billing_context is called standalone)
    incident_count = 0  # wire this to your Incident model when ready

    return {
        "subscription":      subscription,
        "addons":            addons,
        "active_addon_ids":  active_addon_ids,
        "available_services": available_services,
        "plans":             plans,
        "incident_count":    incident_count,
        "is_admin":          is_tenant_admin(request.user, tenant),
    }