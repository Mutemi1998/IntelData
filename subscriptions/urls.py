from django.urls import path

from . import views

urlpatterns = [
        path("upgrade/<int:plan_id>/", views.upgrade_subscription, name="upgrade_subscription"),
        path("services/<int:service_id>/add/",    views.add_service,    name="add_service"),
        path("services/<int:service_id>/remove/", views.remove_service, name="remove_service"),
        path("plans/",                          views.plan_list,             name="plan_list"),
        path("current/",                        views.current_subscription,  name="current_subscription"),
        path("catalog/",                        views.service_catalog,       name="service_catalog"),
]