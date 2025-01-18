from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from operations.models import Operations, ListesParcelles
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

# Create your views here.
def index(request):
    return render(request, 'plateforme_web/index.html')

def souscrire(request):
    # Récupérer les opérations disponibles et actives
    operations_disponibles = Operations.objects.filter(
        Q(disponible=True) & 
        Q(actif=True) &
        Q(date_debut_operation__lte=timezone.now()) &
        (Q(date_fin_operation__gte=timezone.now()) | Q(date_fin_operation__isnull=True))
    ).select_related('projet', 'condition').prefetch_related(
        'types_souscripteurs',
        'types_parcelles',
        'processus_attributions',
        'comptes_bancaires',
        'parcelles'
    ).annotate(
        parcelles_disponibles=Count(
            'parcelles',
            filter=Q(parcelles__actif=True) & Q(parcelles__paye=False)
        )
    )

    context = {
        'operations': operations_disponibles
    }
    return render(request, 'plateforme_web/souscrire.html', context)

def recherche_quittance(request):
    return render(request, 'plateforme_web/recherche_quittance.html')

def etape1_sites(request):
    return render(request, 'plateforme_web/etape1_sites.html')

def etape2_accepter_condition(request):
    # Récupérer les opérations avec leurs conditions
    operations = Operations.objects.filter(
        Q(disponible=True) & 
        Q(actif=True) &
        Q(date_debut_operation__lte=timezone.now()) &
        (Q(date_fin_operation__gte=timezone.now()) | Q(date_fin_operation__isnull=True))
    ).select_related('condition').prefetch_related(
        'types_souscripteurs',
        'types_parcelles'
    )
    
    context = {
        'operations': operations
    }
    return render(request, 'plateforme_web/etape2_accepter_condition.html', context)

def etape3_identification_souscripteur(request):
    return render(request, 'plateforme_web/etape3_identification_souscripteur.html')

def etape4_type_parcelle(request):
    return render(request, 'plateforme_web/etape4_type_parcelle.html')

def etape5_position_parcelle(request):
    return render(request, 'plateforme_web/etape5_position_parcelle.html')

def etape6_paiement(request):
    return render(request, 'plateforme_web/etape6_paiement.html')

def etape7_confirmation_felicitation(request):
    return render(request, 'plateforme_web/etape7_confirmation_felicitation.html')

def generate_pdf(request):
    return render(request, 'plateforme_web/generate_pdf.php')

@require_POST
@csrf_protect
def bloquer_parcelle(request, parcelle_id):
    try:
        parcelle = ListesParcelles.objects.get(id=parcelle_id)
        
        # Vérifier si la parcelle est déjà bloquée
        if parcelle.bloquer:
            return JsonResponse({
                'success': False,
                'message': 'Cette parcelle est déjà bloquée par une autre personne pour souscription'
            }, status=409)
            
        # Si la parcelle n'est pas bloquée, on la bloque
        parcelle.bloquer = True
        parcelle.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Parcelle bloquée avec succès'
        })
        
    except ListesParcelles.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Parcelle non trouvée'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Une erreur est survenue lors du blocage de la parcelle'
        }, status=500)

@require_POST
@csrf_protect
def debloquer_parcelle(request, parcelle_id):
    try:
        parcelle = ListesParcelles.objects.get(id=parcelle_id)
        parcelle.bloquer = False
        parcelle.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Parcelle débloquée avec succès'
        })
        
    except ListesParcelles.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Parcelle non trouvée'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Une erreur est survenue lors du déblocage de la parcelle'
        }, status=500)

@csrf_protect
@require_POST
def marquer_parcelle_payee(request, parcelle_id):
    try:
        parcelle = ListesParcelles.objects.get(id=parcelle_id)
        if parcelle.bloquer and not parcelle.paye:
            parcelle.paye = True
            parcelle.bloquer = False
            parcelle.save()
            return JsonResponse({'status': 'success'})
    except ListesParcelles.DoesNotExist:
        pass
    return JsonResponse({'status': 'error'}, status=400)

def verifier_timer_parcelle(request, parcelle_id):
    cache_key = f'parcelle_timer_{parcelle_id}'
    if not cache.get(cache_key):
        try:
            parcelle = ListesParcelles.objects.get(id=parcelle_id)
            if parcelle.bloquer and not parcelle.paye:
                parcelle.bloquer = False
                parcelle.save()
                return JsonResponse({'status': 'success', 'message': 'Parcelle débloquée'})
        except ListesParcelles.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'}, status=400)
