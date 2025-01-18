from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import re_path
from tableau_administration import views as admin_views


# Ajout de la personnalisation pour le header admin
admin.site.site_header = "Super Admin Souscription SONATUR"
admin.site.index_title = "Super Admin Souscription SONATUR"
admin.site.site_title = "Super Admin Souscription SONATUR"

urlpatterns = [
    path('', include('plateforme_web.urls')),
    path('administration/', RedirectView.as_view(url='/administration/connexion/', permanent=False)),
    path('super_admin/', admin.site.urls),
    path('administration/', include('tableau_administration.urls')),
    path('api/souscriptions/', include('souscriptions.urls')),
    path('api/paiement/initier/', admin_views.initier_paiement, name='initier_paiement'),
    path('api/paiement/verifier/<str:token>/', admin_views.verifier_paiement, name='verifier_paiement'),
    path('api/paiement/callback/', admin_views.callback_paiement, name='callback_paiement'),
]


# Error handlers
from core.erreur_views import (
    handler_400_view, 
    handler_403_view, 
    handler_404_view, 
    handler_500_view
)
handler400 = handler_400_view
handler403 = handler_403_view
handler404 = handler_404_view
handler500 = handler_500_view

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)