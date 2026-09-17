from .models import SubscriptionService

def tenant_has_service(
    tenant,
    service_code
):
    subscription = tenant.subscription

    if subscription.plan.services.filter(
        code=service_code,
        active=True
    ).exists():
        return True

    return SubscriptionService.objects.filter(
        subscription=subscription,
        service__code=service_code,
        enabled=True
    ).exists()