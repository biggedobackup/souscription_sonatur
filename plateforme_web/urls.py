from django.urls import path
from . import views

app_name = 'plateforme_web'

urlpatterns = [
    path('', views.index, name='index'),
    path('souscrire/', views.souscrire, name='souscrire'),
    path('recherche-quittance/', views.recherche_quittance, name='recherche_quittance'),
    path('souscrire/generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('etape1_sites/', views.etape1_sites, name='etape1_sites'),
    path('etape2_accepter_condition/', views.etape2_accepter_condition, name='etape2_accepter_condition'),
    path('etape3_identification_souscripteur/', views.etape3_identification_souscripteur, name='etape3_identification_souscripteur'),
    path('etape4_type_parcelle/', views.etape4_type_parcelle, name='etape4_type_parcelle'),
    path('etape5_position_parcelle/', views.etape5_position_parcelle, name='etape5_position_parcelle'),
    path('etape6_paiement/', views.etape6_paiement, name='etape6_paiement'),
    path('etape7_confirmation_felicitation/', views.etape7_confirmation_felicitation, name='etape7_confirmation_felicitation'),
    path('bloquer_parcelle/<int:parcelle_id>/', views.bloquer_parcelle, name='bloquer_parcelle'),
    path('debloquer_parcelle/<int:parcelle_id>/', views.debloquer_parcelle, name='debloquer_parcelle'),
    path('marquer_parcelle_payee/<int:parcelle_id>/', views.marquer_parcelle_payee, name='marquer_parcelle_payee'),
    path('verifier_timer_parcelle/<int:parcelle_id>/', views.verifier_timer_parcelle, name='verifier_timer_parcelle'),
]
