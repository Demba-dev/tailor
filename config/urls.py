"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.commandes.views import get_commande_details



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/commandes/<int:pk>/details/', get_commande_details, name='api_commande_details'),
    path('core/', include('apps.core.urls')),
    path('clients/', include('apps.clients.urls')),
    path('mesures/', include('apps.mesures.urls')),
    path('commandes/', include('apps.commandes.urls')),
    path('paiements/', include('apps.paiements.urls')),
    path('personnel/', include('apps.personnel.urls')),
    path('formations/', include('apps.formations.urls')),
    path('tissus/', include('apps.tissus.urls')),
    path('modeles/', include('apps.modeles.urls')),
    path('', include('apps.dashboard.urls')),
    path('catalogue/', include('apps.catalogue.urls')),
    path('panier/', include('apps.panier.urls')),
    path('ventes/', include('apps.ventes.urls')),
    path('users/', include('apps.users.urls')),
    path('messages/', include('apps.messagerie.urls')),
    path('settings/', include('apps.settings.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'static'
    )
