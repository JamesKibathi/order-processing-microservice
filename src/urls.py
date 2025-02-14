"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

public_apis = [
    re_path(r"^api/v1/", include('api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="E-COMMERCE SERVICE API DOCS",
        default_version="v1",
        description="E-COMMERCE APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="knjenga94@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=public_apis,
)

docs = [
    re_path(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
]


urlpatterns = (
    public_apis
    + docs
    +[
     path('admin/', admin.site.urls),
])
