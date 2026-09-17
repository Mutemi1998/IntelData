from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts import models


@login_required
def dashboard(request):

    memberships = models.TenantUser.objects.filter(user=request.user).select_related("tenant")

    return render(
        request,
        "soc/dashboard.html",
        {
            "memberships": memberships,
        }
    )


# def index(request):
#     return HttpResponse("Hello, world. You're at the soc index.")