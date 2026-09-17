from datetime import timedelta
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import TenantUser
from customers.models import Domain, Tenant
from django.utils.text import slugify
from .forms import LoginForm, RegisterForm
from django.utils import timezone
from subscriptions.models import (
    Subscription,
    SubscriptionPlan,
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )

@transaction.atomic
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            organization_name = form.cleaned_data[
                "organization_name"
            ]

            schema_name = generate_unique_schema_name(
                organization_name
            )

            # Create tenant
            tenant = Tenant(
                schema_name=schema_name,
                name=organization_name,
            )

            tenant.save()

            # Create domain
            domain_name = f"{schema_name}.localhost"

            Domain.objects.create(
                domain=domain_name,
                tenant=tenant,
                is_primary=True
            )

            # Make registering user tenant admin
            TenantUser.objects.create(
                tenant=tenant,
                user=user,
                role="tenant_admin"
            )
            #create subscription for tenant

            trial_plan = SubscriptionPlan.objects.get(
                name="Trial"
            )

            Subscription.objects.create(
                tenant=tenant,
                plan=trial_plan,
                status="trial",
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=14),
            )

            login(request, user)

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )



@login_required
def logout_view(request):

    logout(request)

    return redirect("login")



def generate_unique_schema_name(name):

    base = slugify(name).replace("-", "_")

    schema_name = base

    counter = 1

    while Tenant.objects.filter(
        schema_name=schema_name
    ).exists():

        counter += 1

        schema_name = f"{base}_{counter}"

    return schema_name
