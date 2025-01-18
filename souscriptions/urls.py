from django.urls import path
from . import views

urlpatterns = [
    # ... existing urls ...
    path('generate_pdf/<str:numero_transaction>/', views.generate_quittance_pdf, name='generate_pdf'),
]