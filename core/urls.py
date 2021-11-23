"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# Django imports
from core import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# Third party imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# My Imports


schema_view = get_schema_view(
    openapi.Info(
        title="tradeit api",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.tradeit.com/policies/terms/",
        contact=openapi.Contact(email="contact@tradeit.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Thrid party stuff
    
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    
    # My Stuff
    path('admin/', admin.site.urls),
    path('api/v1.0/', include('apps.urls',namespace='app')),
    path('auth/', include('apps.account.urls',namespace='account')),
    path('product/', include('apps.product.urls',namespace='product')),
    path('chat/', include('apps.messenger.urls',namespace='messenger'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)