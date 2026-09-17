from django.urls import path
from . import views

urlpatterns = [
    path("",views.settings,name="settings"
    ),
    path('brand-protection/', views.brand_protection, name='brand-protection')
]