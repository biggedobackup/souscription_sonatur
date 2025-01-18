from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date, timedelta
import pandas as pd
from django.db import transaction
from django.http import JsonResponse
import logging
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.cache import cache
import json
from django.db.models import Sum
from utilisateurs.models import Utilisateur, Role
from operations.models import TypeParcelle
from operations.models import Operations
from operations.models import ProcessusAttribution
from paiements.models import CompteBancaire, Paiement
from operations.models import Localite
from operations.models import PositionParcelle
from souscriptions.models import TypeSouscripteur, SouscripteurMorale
from operations.models import Projet
from souscriptions.models import SouscripteurPhysique
from operations.models import Condition
from paiements.models import ModePaiement
from operations.models import ListesParcelles
from operations.models import Operations as Operation
from operations.models import Condition
from souscriptions.models import SouscriptionEffectuee
from django.core.paginator import Paginator
import requests
from django.conf import settings
from django.utils import timezone
import threading
import time
from django.db import connection

# Configurer le logger
logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url='tableau_administration:connexion')
def header(request):
    context = {
        'user': request.user  # Passer l'utilisateur connecté au template
    }
    return render(request, 'tableau_administration/header.html', context)

@login_required(login_url='tableau_administration:connexion')
def footer(request):
    return render(request, 'tableau_administration/footer.html')

@login_required(login_url='tableau_administration:connexion')
def profil(request):
    if request.method == 'POST':
        # Gestion du changement de mot de passe
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        
        if password:
            if password != password_confirmation:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
            elif len(password) < 8:
                messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
            elif password.isnumeric():
                messages.error(request, 'Le mot de passe ne peut pas être entièrement numérique.')
            else:
                request.user.set_password(password)
                request.user.save()
                messages.success(request, 'Mot de passe modifié avec succès.')
                # Reconnecter l'utilisateur avec le nouveau mot de passe
                user = authenticate(username=request.user.email, password=password)
                if user:
                    login(request, user)
                    
    context = {
        'user': request.user  # Passer l'utilisateur connecté au template
    }
    return render(request, 'tableau_administration/profil.html', context)

def connexion(request):
    if request.user.is_authenticated:
        return redirect('tableau_administration:tableau')
        
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'tableau_administration/connexion.html')
            
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            messages.error(request, 'Aucun compte ne correspond à cet email.')
            return render(request, 'tableau_administration/connexion.html')
            
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                allowed_roles = ['Administrateur', 'Moderateur']
                if user.is_superuser or user.is_staff or (user.role and user.role.nom in allowed_roles):
                    login(request, user)
                    messages.success(request, f'Bienvenue à vous {user.nom_complet} !')
                    next_page = request.GET.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect('tableau_administration:tableau')
                else:
                    messages.error(request, 'Vous n\'avez pas les droits d\'accès à l\'administration.')
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            messages.error(request, 'Mot de passe incorrect.')
            
    return render(request, 'tableau_administration/connexion.html')

@login_required(login_url='tableau_administration:connexion')
def deconnexion(request):
    logout(request)
    return redirect('tableau_administration:connexion')

@login_required(login_url='tableau_administration:connexion')
def tableau(request):
    # Ajouter le message de bienvenue
    messages.success(request, f'BIENVENUE\n{request.user.nom_complet}')
    
    # Récupérer les 5 derniers projets
    derniers_projets = Projet.objects.all().order_by('-date_creation')[:5]
    
    # Données pour le diagramme circulaire (répartition des souscripteurs)
    total_souscripteurs_physiques = SouscripteurPhysique.objects.count()
    total_souscripteurs_moraux = SouscripteurMorale.objects.count()
    
    # Données pour le diagramme en bandes (paiements par statut)
    paiements_confirmes = Paiement.objects.filter(statut='confirme').count()
    paiements_en_attente = Paiement.objects.filter(statut='en_attente').count()
    paiements_annules = Paiement.objects.filter(statut='annule').count()
    
    # Données pour le diagramme rectangulaire (parcelles par statut)
    parcelles_actives = ListesParcelles.objects.filter(actif=True, bloquer=False, paye=False).count()
    parcelles_bloquees = ListesParcelles.objects.filter(bloquer=True, paye=False).count()
    parcelles_payees = ListesParcelles.objects.filter(paye=True).count()
    
    # Ajouter ces lignes pour les opérations
    operations_actives = Operations.objects.filter(actif=True).count()
    operations_inactives = Operations.objects.filter(actif=False).count()
    
    context = {
        'total_utilisateurs': Utilisateur.objects.count(),
        'utilisateurs_actifs': Utilisateur.objects.filter(is_active=True).count(),
        'total_types_parcelles': TypeParcelle.objects.count(),
        'total_processus_attribution': ProcessusAttribution.objects.count(),
        'total_comptes_bancaires': CompteBancaire.objects.count(),
        'total_localites': Localite.objects.count(),
        'total_positions_parcelles': PositionParcelle.objects.count(),
        'total_types_souscripteurs': TypeSouscripteur.objects.count(),
        'total_projets': Projet.objects.count(),
        'projets_actifs': Projet.objects.filter(actif=True).count(),
        'total_souscripteurs_moraux': total_souscripteurs_moraux,
        'total_souscripteurs_physiques': total_souscripteurs_physiques,
        'derniers_projets': derniers_projets,  
        'total_modes_paiement': ModePaiement.objects.count(),
        'total_parcelles': ListesParcelles.objects.count(),
        'total_operations': Operations.objects.count(),
        'total_souscriptions': SouscriptionEffectuee.objects.count(),
        'total_paiements': Paiement.objects.count(),
        
        # Données pour les diagrammes
        'donnees_souscripteurs': {
            'physiques': total_souscripteurs_physiques,
            'moraux': total_souscripteurs_moraux
        },
        'donnees_paiements': {
            'confirmes': paiements_confirmes,
            'en_attente': paiements_en_attente,
            'annules': paiements_annules
        },
        'donnees_parcelles': {
            'actives': parcelles_actives,
            'bloquees': parcelles_bloquees,
            'payees': parcelles_payees
        },
        'donnees_operations': {
            'actives': operations_actives,
            'inactives': operations_inactives
        }
    }
    return render(request, 'tableau_administration/tableau.html', context)

@login_required(login_url='tableau_administration:connexion')
def liste_utilisateurs(request):
    search_query = request.GET.get('search', '')
    
    utilisateurs = Utilisateur.objects.all()
    if search_query:
        utilisateurs = utilisateurs.filter(
            Q(email__icontains=search_query) |
            Q(nom_complet__icontains=search_query)
        )
    
    paginator = Paginator(utilisateurs, 10)
    page = request.GET.get('page')
    utilisateurs = paginator.get_page(page)
    
    roles = Role.objects.all()
    
    context = {
        'utilisateurs': utilisateurs,
        'search_query': search_query,
        'roles': roles,
    }
    
    return render(request, 'tableau_administration/liste_utilisateurs.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_utilisateur(request):
    if request.method == 'POST':
        nom_complet = request.POST.get('nom_complet')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        
        try:
            # Vérifier si le rôle existe
            if not role_id:
                raise ValueError('Le rôle est obligatoire')
            
            role = Role.objects.get(id=role_id)
            
            utilisateur = Utilisateur.objects.create_user(
                email=email,
                password=password,
                nom_complet=nom_complet,
                actif=True,
                role=role  # Assigner le rôle directement à la création
            )
            
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('tableau_administration:liste_utilisateurs')
            
        except Role.DoesNotExist:
            messages.error(request, 'Le rôle sélectionné n\'existe pas.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_utilisateurs')

@login_required(login_url='tableau_administration:connexion')
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    
    if request.method == 'POST':
        try:
            utilisateur.nom_complet = request.POST.get('nom_complet')
            utilisateur.email = request.POST.get('email')
            
            # Gestion du mot de passe
            password = request.POST.get('password')
            if password:
                utilisateur.set_password(password)
                
            role_id = request.POST.get('role')
            if role_id:
                utilisateur.role = Role.objects.get(id=role_id)
            utilisateur.actif = 'is_active' in request.POST
            utilisateur.save(update_fields=['nom_complet', 'email', 'role', 'actif'])
            
            messages.success(request, 'Utilisateur modifié avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_utilisateurs')

@login_required(login_url='tableau_administration:connexion')
def supprimer_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    
    try:
        utilisateur.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_utilisateurs')

@login_required(login_url='tableau_administration:connexion')
def liste_types_parcelles(request):
    search_query = request.GET.get('search', '')
    
    types_parcelles = TypeParcelle.objects.all().order_by('code')
    if search_query:
        types_parcelles = types_parcelles.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator_instance = Paginator(types_parcelles, 10)
    page = request.GET.get('page')
    types_parcelles = paginator_instance.get_page(page)
    
    context = {
        'types_parcelles': types_parcelles,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_types_parcelles.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_type_parcelle(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        
        try:
            if not nom:
                raise ValueError('Le nom est obligatoire')
            
            type_parcelle = TypeParcelle.objects.create(
                code=code,
                nom=nom,
                description=description
            )
            
            messages.success(request, 'Type de parcelle créé avec succès.')
            return redirect('tableau_administration:liste_types_parcelles')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_types_parcelles')

@login_required(login_url='tableau_administration:connexion')
def modifier_type_parcelle(request, type_id):
    type_parcelle = get_object_or_404(TypeParcelle, id=type_id)
    
    if request.method == 'POST':
        try:
            type_parcelle.nom = request.POST.get('nom')
            type_parcelle.description = request.POST.get('description')
            type_parcelle.code = request.POST.get('code')
            type_parcelle.save()
            
            messages.success(request, 'Type de parcelle modifié avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_types_parcelles')

@login_required(login_url='tableau_administration:connexion')
def supprimer_type_parcelle(request, type_id):
    type_parcelle = get_object_or_404(TypeParcelle, id=type_id)
    
    try:
        type_parcelle.delete()
        messages.success(request, 'Type de parcelle supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_types_parcelles')

@login_required(login_url='tableau_administration:connexion')
def liste_processus_attribution(request):
    search_query = request.GET.get('search', '')
    
    processus = ProcessusAttribution.objects.all().order_by('-date_creation')
    if search_query:
        processus = processus.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(processus, 10)
    page = request.GET.get('page')
    processus = paginator.get_page(page)
    
    context = {
        'processus': processus,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_processus_attribution.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_processus_attribution(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        
        try:
            if not nom:
                raise ValueError('Le nom est obligatoire')
            if not code:
                raise ValueError('Le code est obligatoire')
            
            processus = ProcessusAttribution.objects.create(
                code=code,
                nom=nom,
                description=description,
                actif=True
            )
            
            messages.success(request, 'Processus d\'attribution créé avec succès.')
            return redirect('tableau_administration:liste_processus_attribution')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_processus_attribution')

@login_required(login_url='tableau_administration:connexion')
def modifier_processus_attribution(request, processus_id):
    processus = get_object_or_404(ProcessusAttribution, id=processus_id)
    
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            nom = request.POST.get('nom')
            
            if not nom:
                raise ValueError('Le nom est obligatoire')
            if not code:
                raise ValueError('Le code est obligatoire')
            
            processus.code = code
            processus.nom = nom
            processus.description = request.POST.get('description')
            processus.actif = 'is_active' in request.POST
            processus.save()
            
            messages.success(request, 'Processus d\'attribution modifié avec succès.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_processus_attribution')

@login_required(login_url='tableau_administration:connexion')
def supprimer_processus_attribution(request, processus_id):
    processus = get_object_or_404(ProcessusAttribution, id=processus_id)
    
    try:
        nom = processus.nom
        processus.delete()
        messages.success(request, f'Le processus d\'attribution "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_processus_attribution')

@login_required(login_url='tableau_administration:connexion')
def liste_comptes_bancaires(request):
    search_query = request.GET.get('search', '')
    
    comptes = CompteBancaire.objects.all().order_by('nom')
    if search_query:
        comptes = comptes.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query) |
            Q(numero_compte__icontains=search_query)
        )
    
    paginator = Paginator(comptes, 10)
    page = request.GET.get('page')
    comptes = paginator.get_page(page)
    
    context = {
        'comptes': comptes,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_comptes_bancaires.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_compte_bancaire(request):
    if request.method == 'POST':
        try:
            compte = CompteBancaire.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom'),
                description=request.POST.get('description'),
                code_banque=request.POST.get('code_banque'),
                code_guichet=request.POST.get('code_guichet'),
                numero_compte=request.POST.get('numero_compte'),
                rib=request.POST.get('rib'),
                actif=True
            )
            
            if request.FILES.get('image'):
                compte.image = request.FILES['image']
                compte.save()
            
            messages.success(request, 'Compte bancaire créé avec succès.')
            return redirect('tableau_administration:liste_comptes_bancaires')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_comptes_bancaires')

@login_required(login_url='tableau_administration:connexion')
def modifier_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, id=compte_id)
    
    if request.method == 'POST':
        try:
            compte.code = request.POST.get('code')
            compte.nom = request.POST.get('nom')
            compte.description = request.POST.get('description')
            compte.code_banque = request.POST.get('code_banque')
            compte.code_guichet = request.POST.get('code_guichet')
            compte.numero_compte = request.POST.get('numero_compte')
            compte.rib = request.POST.get('rib')
            compte.actif = 'is_active' in request.POST
            
            if request.FILES.get('image'):
                compte.image = request.FILES['image']
                
            compte.save()
            
            messages.success(request, 'Compte bancaire modifié avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_comptes_bancaires')

@login_required(login_url='tableau_administration:connexion')
def supprimer_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, id=compte_id)
    
    try:
        nom = compte.nom
        compte.delete()
        messages.success(request, f'Le compte bancaire "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_comptes_bancaires')

@login_required(login_url='tableau_administration:connexion')
def liste_localites(request):
    search_query = request.GET.get('search', '')
    
    localites = Localite.objects.all().order_by('nom')
    if search_query:
        localites = localites.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query)
        )
    
    paginator = Paginator(localites, 10)
    page = request.GET.get('page')
    localites = paginator.get_page(page)
    
    context = {
        'localites': localites,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_localites.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_localite(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            localite = Localite.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom'),
                description=request.POST.get('description'),
                actif=True
            )
            
            messages.success(request, 'Localité créée avec succès.')
            return redirect('tableau_administration:liste_localites')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_localites')

@login_required(login_url='tableau_administration:connexion')
def modifier_localite(request, localite_id):
    localite = get_object_or_404(Localite, id=localite_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            localite.code = request.POST.get('code')
            localite.nom = request.POST.get('nom')
            localite.description = request.POST.get('description')
            localite.actif = 'is_active' in request.POST
            localite.save()
            
            messages.success(request, 'Localité modifiée avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_localites')

@login_required(login_url='tableau_administration:connexion')
def supprimer_localite(request, localite_id):
    localite = get_object_or_404(Localite, id=localite_id)
    
    try:
        nom = localite.nom
        localite.delete()
        messages.success(request, f'La localité "{nom}" a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_localites')

@login_required(login_url='tableau_administration:connexion')
def liste_positions_parcelles(request):
    search_query = request.GET.get('search', '')
    
    positions = PositionParcelle.objects.all().order_by('nom')
    if search_query:
        positions = positions.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query)
        )
    
    paginator = Paginator(positions, 10)
    page = request.GET.get('page')
    positions = paginator.get_page(page)
    
    # Récupérer tous les types de parcelles pour le formulaire
    types_parcelles = TypeParcelle.objects.filter(actif=True)
    
    context = {
        'positions': positions,
        'search_query': search_query,
        'types_parcelles': types_parcelles,  # Ajout des types de parcelles
    }
    
    return render(request, 'tableau_administration/liste_positions_parcelles.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_position_parcelle(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
            if not request.POST.get('type_parcelle'):
                raise ValueError('Le type de parcelle est obligatoire')
                
            type_parcelle = TypeParcelle.objects.get(id=request.POST.get('type_parcelle'))
                
            position = PositionParcelle.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom'),
                description=request.POST.get('description'),
                type_parcelle=type_parcelle,
                actif=True
            )
            
            messages.success(request, 'Position de parcelle créée avec succès.')
            return redirect('tableau_administration:liste_positions_parcelles')
            
        except TypeParcelle.DoesNotExist:
            messages.error(request, 'Le type de parcelle sélectionné n\'existe pas.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_positions_parcelles')

@login_required(login_url='tableau_administration:connexion')
def modifier_position_parcelle(request, position_id):
    position = get_object_or_404(PositionParcelle, id=position_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
            if not request.POST.get('type_parcelle'):
                raise ValueError('Le type de parcelle est obligatoire')
                
            type_parcelle = TypeParcelle.objects.get(id=request.POST.get('type_parcelle'))
                
            position.code = request.POST.get('code')
            position.nom = request.POST.get('nom')
            position.description = request.POST.get('description')
            position.type_parcelle = type_parcelle
            position.actif = 'is_active' in request.POST
            position.save()
            
            messages.success(request, 'Position de parcelle modifiée avec succès.')
        except TypeParcelle.DoesNotExist:
            messages.error(request, 'Le type de parcelle sélectionné n\'existe pas.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_positions_parcelles')

@login_required(login_url='tableau_administration:connexion')
def supprimer_position_parcelle(request, position_id):
    position = get_object_or_404(PositionParcelle, id=position_id)
    
    try:
        nom = position.nom
        position.delete()
        messages.success(request, f'La position de parcelle "{nom}" a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_positions_parcelles')

@login_required(login_url='tableau_administration:connexion')
def liste_types_souscripteurs(request):
    search_query = request.GET.get('search', '')
    
    types = TypeSouscripteur.objects.all().order_by('nom')
    if search_query:
        types = types.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query)
        )
    
    paginator = Paginator(types, 10)
    page = request.GET.get('page')
    types = paginator.get_page(page)
    
    context = {
        'types': types,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_types_souscripteurs.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_type_souscripteur(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            type_souscripteur = TypeSouscripteur.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom'),
                description=request.POST.get('description'),
                actif=True
            )
            
            messages.success(request, 'Type de souscripteur créé avec succès.')
            return redirect('tableau_administration:liste_types_souscripteurs')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_types_souscripteurs')

@login_required(login_url='tableau_administration:connexion')
def modifier_type_souscripteur(request, type_id):
    type_souscripteur = get_object_or_404(TypeSouscripteur, id=type_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            type_souscripteur.code = request.POST.get('code')
            type_souscripteur.nom = request.POST.get('nom')
            type_souscripteur.description = request.POST.get('description')
            type_souscripteur.actif = 'is_active' in request.POST
            type_souscripteur.save()
            
            messages.success(request, 'Type de souscripteur modifié avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_types_souscripteurs')

@login_required(login_url='tableau_administration:connexion')
def supprimer_type_souscripteur(request, type_id):
    type_souscripteur = get_object_or_404(TypeSouscripteur, id=type_id)
    
    try:
        nom = type_souscripteur.nom
        type_souscripteur.delete()
        messages.success(request, f'Le type de souscripteur "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_types_souscripteurs')

@login_required(login_url='tableau_administration:connexion')
def liste_projets(request):
    search_query = request.GET.get('search', '')
    
    projets = Projet.objects.all().order_by('-date_creation')
    if search_query:
        projets = projets.filter(
            Q(code__icontains=search_query) |
            Q(libelle__icontains=search_query)
        )
    
    paginator = Paginator(projets, 10)
    page = request.GET.get('page')
    projets = paginator.get_page(page)
    
    # Récupérer toutes les localités actives pour le formulaire
    localites = Localite.objects.filter(actif=True)
    
    context = {
        'projets': projets,
        'search_query': search_query,
        'localites': localites,
    }
    
    return render(request, 'tableau_administration/liste_projets.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_projet(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('libelle'):
                raise ValueError('Le libellé est obligatoire')
            if not request.POST.get('localite'):
                raise ValueError('La localité est obligatoire')
                
            localite = Localite.objects.get(id=request.POST.get('localite'))
            
            projet = Projet.objects.create(
                code=request.POST.get('code'),
                libelle=request.POST.get('libelle'),
                description=request.POST.get('description'),
                localite=localite,
                date_debut=request.POST.get('date_debut') or None,
                date_fin=request.POST.get('date_fin') or None,
                superficie_origine=request.POST.get('superficie_origine') or 0,
                superficie_viabilisee=request.POST.get('superficie_viabilisee') or 0,
                actif=True,
                archive=False
            )
            
            messages.success(request, 'Projet créé avec succès.')
            return redirect('tableau_administration:liste_projets')
            
        except Localite.DoesNotExist:
            messages.error(request, 'La localité sélectionnée n\'existe pas.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_projets')

@login_required(login_url='tableau_administration:connexion')
def modifier_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('libelle'):
                raise ValueError('Le libellé est obligatoire')
            if not request.POST.get('localite'):
                raise ValueError('La localité est obligatoire')
                
            localite = Localite.objects.get(id=request.POST.get('localite'))
            
            projet.code = request.POST.get('code')
            projet.libelle = request.POST.get('libelle')
            projet.description = request.POST.get('description')
            projet.localite = localite
            projet.date_debut = request.POST.get('date_debut') or None
            projet.date_fin = request.POST.get('date_fin') or None
            
            # Conversion des superficies en float ou 0 si vide
            projet.superficie_origine = float(request.POST.get('superficie_origine') or 0)
            projet.superficie_viabilisee = float(request.POST.get('superficie_viabilisee') or 0)
            
            projet.actif = 'is_active' in request.POST
            projet.archive = 'is_archive' in request.POST
            projet.save()
            
            messages.success(request, 'Projet modifié avec succès.')
        except Localite.DoesNotExist:
            messages.error(request, 'La localité sélectionnée n\'existe pas.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_projets')

@login_required(login_url='tableau_administration:connexion')
def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    
    try:
        libelle = projet.libelle
        projet.delete()
        messages.success(request, f'Le projet "{libelle}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_projets')

@login_required(login_url='tableau_administration:connexion')
def liste_souscripteurs_physiques(request):
    search_query = request.GET.get('search', '')
    
    souscripteurs = SouscripteurPhysique.objects.select_related('type_souscripteur').all().order_by('-date_creation')
    if search_query:
        souscripteurs = souscripteurs.filter(
            Q(nom_complet__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(profession__icontains=search_query) |
            Q(numero_piece__icontains=search_query) |
 
            Q(type_souscripteur__nom__icontains=search_query)
        )
    
    paginator = Paginator(souscripteurs, 10)
    page = request.GET.get('page')
    souscripteurs = paginator.get_page(page)
    
    types_souscripteurs = TypeSouscripteur.objects.filter(actif=True)
    
    context = {
        'souscripteurs': souscripteurs,
        'search_query': search_query,
        'types_souscripteurs': types_souscripteurs,
        'PAYS_CHOICES': SouscripteurPhysique.PAYS_CHOICES,
        'DOCUMENT_CHOICES': SouscripteurPhysique.DOCUMENT_CHOICES,
        'GENRE_CHOICES': SouscripteurPhysique.GENRE_CHOICES,
    }
    
    return render(request, 'tableau_administration/liste_souscripteurs_physiques.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_souscripteur_physique(request):
    if request.method == 'POST':
        try:
            required_fields = ['nom_complet', 'email', 'telephone', 
                             'date_naissance', 'lieu_naissance', 'profession', 'genre', 
                              'document', 'numero_piece']
            
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f'Le champ {field} est obligatoire')
            
            date_naissance = datetime.strptime(request.POST.get('date_naissance'), '%Y-%m-%d').date()
            age = (date.today() - date_naissance).days / 365.25
            if age < 18:
                raise ValueError('Le souscripteur doit avoir au moins 18 ans')

            date_etablissement = datetime.strptime(request.POST.get('date_etablissement'), '%Y-%m-%d').date()
            date_expiration = datetime.strptime(request.POST.get('date_expiration'), '%Y-%m-%d').date()
            if date_expiration <= date_etablissement:
                raise ValueError('La date d\'expiration doit être postérieure à la date d\'établissement')

            souscripteur = SouscripteurPhysique.objects.create(
                nom_complet=request.POST.get('nom_complet'),
                email=request.POST.get('email'),
                telephone=request.POST.get('telephone'),
                date_naissance=date_naissance,
                lieu_naissance=request.POST.get('lieu_naissance'),
                profession=request.POST.get('profession'),
                genre=request.POST.get('genre'),
                document=request.POST.get('document'),
                numero_piece=request.POST.get('numero_piece'),
                date_expiration=date_expiration,
                lieu_etablissement=request.POST.get('lieu_etablissement'),
                date_etablissement=date_etablissement,
                pays=request.POST.get('pays'),
                region=request.POST.get('region'),
                ville=request.POST.get('ville'),
                adresse=request.POST.get('adresse'),
                actif=True
            )
            
            messages.success(request, 'Souscripteur physique créé avec succès.')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_souscripteurs_physiques')

@login_required(login_url='tableau_administration:connexion')
def modifier_souscripteur_physique(request, souscripteur_id):
    souscripteur = get_object_or_404(SouscripteurPhysique, id=souscripteur_id)
    
    if request.method == 'POST':
        try:
            souscripteur.nom_complet = request.POST.get('nom_complet')
            souscripteur.email = request.POST.get('email')
            souscripteur.telephone = request.POST.get('telephone')
            souscripteur.date_naissance = datetime.strptime(request.POST.get('date_naissance'), '%Y-%m-%d').date()
            souscripteur.lieu_naissance = request.POST.get('lieu_naissance')
            souscripteur.profession = request.POST.get('profession')
            souscripteur.genre = request.POST.get('genre')
            souscripteur.document = request.POST.get('document')
            souscripteur.numero_piece = request.POST.get('numero_piece')
            souscripteur.date_expiration = datetime.strptime(request.POST.get('date_expiration'), '%Y-%m-%d').date()
            souscripteur.lieu_etablissement = request.POST.get('lieu_etablissement')
            souscripteur.date_etablissement = datetime.strptime(request.POST.get('date_etablissement'), '%Y-%m-%d').date()
            souscripteur.pays = request.POST.get('pays')
            souscripteur.region = request.POST.get('region')
            souscripteur.ville = request.POST.get('ville')
            souscripteur.adresse = request.POST.get('adresse')
            souscripteur.actif = 'is_active' in request.POST
            souscripteur.save()
            
            messages.success(request, 'Souscripteur physique modifié avec succès.')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_souscripteurs_physiques')

@login_required(login_url='tableau_administration:connexion')
def supprimer_souscripteur_physique(request, souscripteur_id):
    souscripteur = get_object_or_404(SouscripteurPhysique, id=souscripteur_id)
    
    try:
        nom = souscripteur.nom_complet
        souscripteur.delete()
        messages.success(request, f'Le souscripteur physique "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_souscripteurs_physiques')

@login_required(login_url='tableau_administration:connexion')
def liste_conditions(request):
    search_query = request.GET.get('search', '')
    
    conditions = Condition.objects.select_related('operation').all()
    if search_query:
        conditions = conditions.filter(
            Q(code__icontains=search_query) |
            Q(intitule__icontains=search_query) |
            Q(operation__intitule__icontains=search_query)
        )
    
    paginator = Paginator(conditions, 10)
    page = request.GET.get('page')
    conditions = paginator.get_page(page)
    
    # Récupérer uniquement les opérations actives
    operations = Operations.objects.filter(actif=True)
    
    context = {
        'conditions': conditions,
        'search_query': search_query,
        'operations': operations,
    }
    
    return render(request, 'tableau_administration/liste_conditions.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_condition(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('intitule'):
                raise ValueError('L\'intitulé est obligatoire')
            if not request.POST.get('operation'):
                raise ValueError('L\'opération est obligatoire')
                
            operation = Operations.objects.get(id=request.POST.get('operation'))
            
            condition = Condition.objects.create(
                code=request.POST.get('code'),
                intitule=request.POST.get('intitule'),
                condition_souscription=request.POST.get('condition_souscription'),
                methode_attribution=request.POST.get('methode_attribution'),
                documents_requis=request.POST.get('documents_requis'),
                operation=operation,
                actif=True
            )
            
            messages.success(request, 'Condition créée avec succès.')
            return redirect('tableau_administration:liste_conditions')
            
        except Operations.DoesNotExist:
            messages.error(request, 'L\'opération sélectionnée n\'existe pas.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_conditions')

@login_required(login_url='tableau_administration:connexion')
def modifier_condition(request, condition_id):
    condition = get_object_or_404(Condition, id=condition_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('intitule'):
                raise ValueError('L\'intitulé est obligatoire')
            if not request.POST.get('operation'):
                raise ValueError('L\'opération est obligatoire')
                
            operation = Operations.objects.get(id=request.POST.get('operation'))
            
            condition.code = request.POST.get('code')
            condition.intitule = request.POST.get('intitule')
            condition.condition_souscription = request.POST.get('condition_souscription')
            condition.methode_attribution = request.POST.get('methode_attribution')
            condition.documents_requis = request.POST.get('documents_requis')
            condition.operation = operation
            condition.actif = 'is_active' in request.POST
            condition.save()
            
            messages.success(request, 'Condition modifiée avec succès.')
        except Operations.DoesNotExist:
            messages.error(request, 'L\'opération sélectionnée n\'existe pas.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_conditions')

@login_required(login_url='tableau_administration:connexion')
def supprimer_condition(request, condition_id):
    condition = get_object_or_404(Condition, id=condition_id)
    
    try:
        intitule = condition.intitule
        condition.delete()
        messages.success(request, f'La condition "{intitule}" a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_conditions')

@login_required(login_url='tableau_administration:connexion')
def liste_modes_paiement(request):
    search_query = request.GET.get('search', '')
    
    modes_paiement = ModePaiement.objects.all().order_by('code')
    if search_query:
        modes_paiement = modes_paiement.filter(
            Q(code__icontains=search_query) |
            Q(nom__icontains=search_query) 
        )
    
    paginator = Paginator(modes_paiement, 10)
    page = request.GET.get('page')
    modes_paiement = paginator.get_page(page)
    
    context = {
        'modes_paiement': modes_paiement,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_modes_paiement.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_mode_paiement(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            mode_paiement = ModePaiement.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom'),
                actif=True
            )
            
            messages.success(request, 'Mode de paiement créé avec succès.')
            return redirect('tableau_administration:liste_modes_paiement')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_modes_paiement')

@login_required(login_url='tableau_administration:connexion')
def modifier_mode_paiement(request, mode_id):
    mode_paiement = get_object_or_404(ModePaiement, id=mode_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
            if not request.POST.get('nom'):
                raise ValueError('Le nom est obligatoire')
                
            mode_paiement.code = request.POST.get('code')
            mode_paiement.nom = request.POST.get('nom')
            mode_paiement.actif = 'is_active' in request.POST
            mode_paiement.save()
            
            messages.success(request, 'Mode de paiement modifié avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_modes_paiement')

@login_required(login_url='tableau_administration:connexion')
def supprimer_mode_paiement(request, mode_id):
    mode_paiement = get_object_or_404(ModePaiement, id=mode_id)
    
    try:
        nom = mode_paiement.nom
        mode_paiement.delete()
        messages.success(request, f'Le mode de paiement "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_modes_paiement')

@login_required(login_url='tableau_administration:connexion')
def liste_parcelles(request):
    search_query = request.GET.get('search', '')
    
    parcelles = ListesParcelles.objects.all().order_by('-date_ajout')
    if search_query:
        parcelles = parcelles.filter(
            Q(code__icontains=search_query) |
            Q(site__icontains=search_query) |
            Q(zone__icontains=search_query) |
            Q(parcelle__icontains=search_query)
        )
    
    paginator = Paginator(parcelles, 10)
    page = request.GET.get('page')
    parcelles = paginator.get_page(page)
    
    operations = Operations.objects.all()
    
    context = {
        'parcelles': parcelles,
        'operations': operations,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_parcelles.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_parcelle(request):
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
                
            operation = None
            if request.POST.get('operation'):
                operation = Operations.objects.get(id=request.POST.get('operation'))
            
            try:
                surface = int(request.POST.get('surface', 0))
                cout_m2 = int(request.POST.get('cout_m2', 0))
                acompte = int(request.POST.get('acompte', 0))
                cout_total = int(request.POST.get('cout_total', 0))
                reste_a_payer = int(request.POST.get('reste_a_payer', 0))
            except ValueError:
                raise ValueError('Les valeurs numériques sont invalides')
            
            parcelle = ListesParcelles.objects.create(
                operation=operation,
                code=request.POST.get('code'),
                site=request.POST.get('site'),
                zone=request.POST.get('zone'),
                section=request.POST.get('section'),
                position=request.POST.get('position'),
                lot=request.POST.get('lot'),
                parcelle=request.POST.get('parcelle'),
                usage=request.POST.get('usage'),
                surface=surface,
                cout_m2=cout_m2,
                acompte=acompte,
                cout_total=cout_total,
                reste_a_payer=reste_a_payer,
                actif=True
            )
            
            messages.success(request, 'Parcelle créée avec succès.')
            return redirect('tableau_administration:liste_parcelles')
            
        except Operations.DoesNotExist:
            messages.error(request, 'L\'opération sélectionnée n\'existe pas.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_parcelles')

@login_required(login_url='tableau_administration:connexion')
def modifier_parcelle(request, parcelle_id):
    parcelle = get_object_or_404(ListesParcelles, id=parcelle_id)
    
    if request.method == 'POST':
        try:
            if not request.POST.get('code'):
                raise ValueError('Le code est obligatoire')
                
            operation = None
            if request.POST.get('operation'):
                operation = Operations.objects.get(id=request.POST.get('operation'))
            
            try:
                surface = int(request.POST.get('surface', 0))
                cout_m2 = int(request.POST.get('cout_m2', 0))
                acompte = int(request.POST.get('acompte', 0))
                cout_total = int(request.POST.get('cout_total', 0))
                reste_a_payer = int(request.POST.get('reste_a_payer', 0))
            except ValueError:
                raise ValueError('Les valeurs numériques sont invalides')
            
            parcelle.operation = operation
            parcelle.code = request.POST.get('code')
            parcelle.site = request.POST.get('site')
            parcelle.zone = request.POST.get('zone')
            parcelle.section = request.POST.get('section')
            parcelle.position = request.POST.get('position')
            parcelle.lot = request.POST.get('lot')
            parcelle.parcelle = request.POST.get('parcelle')
            parcelle.usage = request.POST.get('usage')
            parcelle.surface = surface
            parcelle.cout_m2 = cout_m2
            parcelle.acompte = acompte
            parcelle.cout_total = cout_total
            parcelle.reste_a_payer = reste_a_payer
            parcelle.actif = 'is_active' in request.POST
            parcelle.bloquer = 'is_blocked' in request.POST
            parcelle.paye = 'is_paid' in request.POST
            parcelle.save()
            
            messages.success(request, 'Parcelle modifiée avec succès.')
        except Operations.DoesNotExist:
            messages.error(request, 'L\'opération sélectionnée n\'existe pas.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_parcelles')

@login_required(login_url='tableau_administration:connexion')
def supprimer_parcelle(request, parcelle_id):
    parcelle = get_object_or_404(ListesParcelles, id=parcelle_id)
    
    try:
        code = parcelle.code
        parcelle.delete()
        messages.success(request, f'La parcelle "{code}" a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_parcelles')

@login_required(login_url='tableau_administration:connexion')
def importer_parcelles(request):
    if request.method == 'POST' and request.FILES.get('fichier_excel'):
        try:
            excel_file = request.FILES['fichier_excel']
            ignorer_erreurs = request.POST.get('ignorer_erreurs') == 'on'
            operation_id = request.POST.get('operation_id')
            
            # Récupérer l'opération sélectionnée dans le formulaire
            operation_par_defaut = None
            if operation_id:
                try:
                    operation_par_defaut = Operations.objects.get(id=operation_id)
                except Operations.DoesNotExist:
                    raise ValueError("L'opération sélectionnée n'existe pas")
            
            # Lire le fichier Excel
            df = pd.read_excel(excel_file, skiprows=1)
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Vérifier les colonnes requises
            colonnes_requises = ['code', 'site', 'zone', 'section', 'position', 'lot', 
                               'parcelle', 'usage', 'surface', 'cout_m2', 'acompte']
            colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]
            if colonnes_manquantes:
                raise ValueError(f"Colonnes manquantes dans le fichier : {', '.join(colonnes_manquantes)}")
            
            parcelles_created = 0
            parcelles_failed = 0
            erreurs = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Rechercher la position de la parcelle par son code
                        try:
                            position_parcelle = PositionParcelle.objects.get(code=str(row['position']))
                        except PositionParcelle.DoesNotExist:
                            raise ValueError(f"Position de parcelle avec le code {row['position']} non trouvée")

                        # Rechercher le type de parcelle par son code
                        try:
                            type_parcelle = TypeParcelle.objects.get(nom=str(row['usage']))
                        except TypeParcelle.DoesNotExist:
                            raise ValueError(f"Type de parcelle avec le nom {row['usage']} non trouvé")

                        # Créer la parcelle avec la position trouvée
                        parcelle = ListesParcelles.objects.create(
                            operation=operation_par_defaut,
                            code=str(row['code']),
                            site=str(row['site']),
                            zone=str(row['zone']),
                            section=str(row['section']),
                            position=position_parcelle,  # Utiliser l'objet PositionParcelle trouvé
                            lot=str(row['lot']),
                            parcelle=str(row['parcelle']),
                            usage=type_parcelle,
                            surface=int(float(row['surface'])),
                            cout_m2=int(float(row['cout_m2'])),
                            acompte=int(float(row['acompte'])),
                            cout_total=int(float(row['cout_total'])) if 'cout_total' in df.columns else None,
                            reste_a_payer=int(float(row['reste_a_payer'])) if 'reste_a_payer' in df.columns else None,
                            actif=True
                        )
                        parcelles_created += 1
                        
                    except Exception as e:
                        parcelles_failed += 1
                        erreurs.append(f"Ligne {index + 2}: {str(e)}")
                        if not ignorer_erreurs:
                            raise Exception(f"Erreur à la ligne {index + 2}: {str(e)}")
                
            message = f"{parcelles_created} parcelles importées avec succès."
            if parcelles_failed > 0:
                message += f" {parcelles_failed} parcelles en erreur."
                if erreurs:
                    message += f" Détails des erreurs : {', '.join(erreurs)}"
            messages.success(request, message)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {str(e)}")
            
    return redirect('tableau_administration:liste_parcelles')

@login_required(login_url='tableau_administration:connexion')
def liste_souscripteurs_moraux(request):
    search_query = request.GET.get('search', '')
    
    souscripteurs = SouscripteurMorale.objects.select_related('type_souscripteur').all().order_by('-date_creation')
    if search_query:
        souscripteurs = souscripteurs.filter(
            Q(raison_sociale__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(rccm__icontains=search_query) |
            Q(ifu__icontains=search_query) |
            Q(nom_representant__icontains=search_query) |
            Q(prenom_representant__icontains=search_query) |
            Q(type_souscripteur__nom__icontains=search_query)
        )
    
    paginator = Paginator(souscripteurs, 10)
    page = request.GET.get('page')
    souscripteurs = paginator.get_page(page)
    
    types_souscripteurs = TypeSouscripteur.objects.filter(actif=True)
    
    context = {
        'souscripteurs': souscripteurs,
        'search_query': search_query,
        'types_souscripteurs': types_souscripteurs,
        'PAYS_CHOICES': SouscripteurPhysique.PAYS_CHOICES,
        'FORME_JURIDIQUE_CHOICES': SouscripteurMorale.FORME_JURIDIQUE_CHOICES,
    }
    
    return render(request, 'tableau_administration/liste_souscripteurs_moraux.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_souscripteur_moral(request):
    if request.method == 'POST':
        try:
            required_fields = ['raison_sociale', 'forme_juridique', 'siege_social', 
                             'nom_representant', 'prenom_representant', 'fonction_representant',
                             'telephone', 'email']
            
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f'Le champ {field} est obligatoire')

            souscripteur = SouscripteurMorale.objects.create(
                raison_sociale=request.POST.get('raison_sociale'),
                forme_juridique=request.POST.get('forme_juridique'),
                rccm=request.POST.get('rccm'),
                ifu=request.POST.get('ifu'),
                siege_social=request.POST.get('siege_social'),
                nom_representant=request.POST.get('nom_representant'),
                prenom_representant=request.POST.get('prenom_representant'),
                fonction_representant=request.POST.get('fonction_representant'),
                telephone=request.POST.get('telephone'),
                email=request.POST.get('email'),
                pays=request.POST.get('pays'),
                region=request.POST.get('region'),
                ville=request.POST.get('ville'),
                adresse=request.POST.get('adresse'),
                actif=True
            )
            
            messages.success(request, 'Souscripteur moral créé avec succès.')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_souscripteurs_moraux')

@login_required(login_url='tableau_administration:connexion')
def modifier_souscripteur_moral(request, souscripteur_id):
    souscripteur = get_object_or_404(SouscripteurMorale, id=souscripteur_id)
    
    if request.method == 'POST':
        try:
            souscripteur.raison_sociale = request.POST.get('raison_sociale')
            souscripteur.forme_juridique = request.POST.get('forme_juridique')
            souscripteur.rccm = request.POST.get('rccm')
            souscripteur.ifu = request.POST.get('ifu')
            souscripteur.siege_social = request.POST.get('siege_social')
            souscripteur.nom_representant = request.POST.get('nom_representant')
            souscripteur.prenom_representant = request.POST.get('prenom_representant')
            souscripteur.fonction_representant = request.POST.get('fonction_representant')
            souscripteur.telephone = request.POST.get('telephone')
            souscripteur.email = request.POST.get('email')
            souscripteur.pays = request.POST.get('pays')
            souscripteur.region = request.POST.get('region')
            souscripteur.ville = request.POST.get('ville')
            souscripteur.adresse = request.POST.get('adresse')
            souscripteur.actif = 'is_active' in request.POST
            souscripteur.save()
            
            messages.success(request, 'Souscripteur moral modifié avec succès.')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_souscripteurs_moraux')

@login_required(login_url='tableau_administration:connexion')
def supprimer_souscripteur_moral(request, souscripteur_id):
    souscripteur = get_object_or_404(SouscripteurMorale, id=souscripteur_id)
    
    try:
        nom = souscripteur.raison_sociale
        souscripteur.delete()
        messages.success(request, f'Le souscripteur moral "{nom}" a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_souscripteurs_moraux')

@login_required(login_url='tableau_administration:connexion')
def liste_operations(request):
    search_query = request.GET.get('search', '')
    
    operations = Operations.objects.select_related('projet', 'condition').prefetch_related(
        'positions_parcelles',
        'types_souscripteurs',
        'types_parcelles',
        'processus_attributions',
        'comptes_bancaires'
    ).all().order_by('-date_debut_operation')
    
    paginator = Paginator(operations, 10)
    page = request.GET.get('page')
    operations = paginator.get_page(page)
    
    # Récupérer les données pour les dropdowns
    projets = Projet.objects.filter(actif=True)
    types_souscripteurs = TypeSouscripteur.objects.filter(actif=True)
    types_parcelles = TypeParcelle.objects.filter(actif=True)
    processus_attributions = ProcessusAttribution.objects.filter(actif=True)
    comptes_bancaires = CompteBancaire.objects.filter(actif=True)
    
    context = {
        'operations': operations,
        'search_query': search_query,
        'projets': projets,
        'types_souscripteurs': types_souscripteurs,
        'types_parcelles': types_parcelles,
        'processus_attributions': processus_attributions,
        'comptes_bancaires': comptes_bancaires,
        'positions_parcelles': PositionParcelle.objects.filter(actif=True),
    }
    
    return render(request, 'tableau_administration/liste_operations.html', context)

@login_required(login_url='tableau_administration:connexion')
def ajouter_operation(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Vérification des champs requis
                required_fields = ['code', 'intitule', 'projet', 'date_debut_operation']
                for field in required_fields:
                    if not request.POST.get(field):
                        raise ValueError(f'Le champ {field} est obligatoire')

                # Création de l'opération
                operation = Operations.objects.create(
                    code=request.POST.get('code'),
                    intitule=request.POST.get('intitule'),
                    projet_id=request.POST.get('projet'),
                    description=request.POST.get('description'),
                    date_debut_operation=request.POST.get('date_debut_operation'),
                    date_fin_operation=request.POST.get('date_fin_operation') or None,
                    duree_depot_physique=int(request.POST.get('duree_depot_physique') or 0),
                    duree_souscription=int(request.POST.get('duree_souscription') or 0),
                    montant_souscription=int(request.POST.get('montant_souscription') or 0),
                    disponible=request.POST.get('disponible') == 'on',
                    actif=True
                )

                # Gestion du visuel
                if request.FILES.get('visuel'):
                    operation.visuel = request.FILES['visuel']
                    operation.save()

                # Ajout des relations many-to-many
                if request.POST.getlist('types_souscripteurs'):
                    operation.types_souscripteurs.set(request.POST.getlist('types_souscripteurs'))
                if request.POST.getlist('types_parcelles'):
                    operation.types_parcelles.set(request.POST.getlist('types_parcelles'))
                if request.POST.getlist('processus_attributions'):
                    operation.processus_attributions.set(request.POST.getlist('processus_attributions'))
                if request.POST.getlist('comptes_bancaires'):
                    operation.comptes_bancaires.set(request.POST.getlist('comptes_bancaires'))

                # Création de la condition associée
                if any([request.POST.get('condition_code'), 
                       request.POST.get('condition_intitule'),
                       request.POST.get('condition_souscription'),
                       request.POST.get('methode_attribution'),
                       request.POST.get('documents_requis')]):
                    
                    # Vérifier les champs requis de la condition
                    if not all([request.POST.get('condition_code'),
                              request.POST.get('condition_intitule')]):
                        raise ValueError('Le code et l\'intitulé de la condition sont obligatoires')
                        
                    condition = Condition.objects.create(
                        code=request.POST.get('condition_code'),
                        intitule=request.POST.get('condition_intitule'),
                        condition_souscription=request.POST.get('condition_souscription', ''),
                        methode_attribution=request.POST.get('methode_attribution', ''),
                        documents_requis=request.POST.get('documents_requis', ''),
                        operation=operation,
                        actif=True
                    )
                    operation.condition = condition
                    operation.save()

                # Import des parcelles
                if request.FILES.get('fichier_parcelles'):
                    try:
                        df = pd.read_excel(request.FILES['fichier_parcelles'], skiprows=1)
                        df.columns = df.columns.str.lower().str.replace(' ', '_')
                        
                        # Vérifier les colonnes requises
                        required_columns = ['code', 'site', 'zone', 'section', 'position', 
                                         'lot', 'parcelle', 'usage', 'surface', 'cout_m2', 
                                         'acompte']
                        
                        missing_columns = [col for col in required_columns if col not in df.columns]
                        if missing_columns:
                            raise ValueError(f"Colonnes manquantes dans le fichier: {', '.join(missing_columns)}")
                            
                        parcelles_importees = []
                        erreurs = []
                        positions_ids = set()  # Pour stocker les IDs des positions

                        for index, row in df.iterrows():
                            try:
                                # Rechercher la position de la parcelle par son code
                                try:
                                    position_parcelle = PositionParcelle.objects.get(code=str(row['position']))
                                    positions_ids.add(position_parcelle.id)  # Ajouter l'ID à l'ensemble
                                except PositionParcelle.DoesNotExist:
                                    raise ValueError(f"Position de parcelle avec le code {row['position']} non trouvée")

                                # Rechercher le type de parcelle par son code
                                try:
                                    type_parcelle = TypeParcelle.objects.get(nom=str(row['usage']))
                                except TypeParcelle.DoesNotExist:
                                    raise ValueError(f"Type de parcelle avec le nom {row['usage']} non trouvé")

                                parcelle = ListesParcelles.objects.create(
                                    operation=operation,
                                    code=str(row['code']),
                                    site=str(row['site']),
                                    zone=str(row['zone']),
                                    section=str(row['section']),
                                    position=position_parcelle,
                                    lot=str(row['lot']),
                                    parcelle=str(row['parcelle']),
                                    usage=type_parcelle,
                                    surface=int(float(row['surface'])),
                                    cout_m2=int(float(row['cout_m2'])),
                                    acompte=int(float(row['acompte'])),
                                    cout_total=int(float(row['cout_total'])) if 'cout_total' in df.columns else None,
                                    reste_a_payer=int(float(row['reste_a_payer'])) if 'reste_a_payer' in df.columns else None,
                                    actif=True
                                )
                                parcelles_importees.append(parcelle.id)
                            except Exception as e:
                                erreurs.append(f"Ligne {index + 2}: {str(e)}")

                        if erreurs:
                            raise ValueError("\n".join(erreurs))

                        # Associer les parcelles importées à l'opération
                        # Garder les parcelles existantes et ajouter les nouvelles
                        existing_parcelles = set(operation.parcelles.values_list('id', flat=True))
                        all_parcelles = existing_parcelles.union(parcelles_importees)
                        operation.parcelles.set(all_parcelles)

                        # Ajouter les positions de parcelles à l'opération
                        if positions_ids:
                            # Garder les positions existantes et ajouter les nouvelles
                            existing_positions = set(operation.positions_parcelles.values_list('id', flat=True))
                            all_positions = existing_positions.union(positions_ids)
                            operation.positions_parcelles.set(all_positions)

                    except Exception as e:
                        raise ValueError(f"Erreur lors de l'import des parcelles: {str(e)}")

            messages.success(request, 'Opération créée avec succès.')
            return redirect('tableau_administration:liste_operations')

        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            
    return redirect('tableau_administration:liste_operations')

@login_required(login_url='tableau_administration:connexion')
def modifier_operation(request, operation_id):
    operation = get_object_or_404(Operations, id=operation_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Mise à jour des champs de base
                operation.code = request.POST.get('code')
                operation.intitule = request.POST.get('intitule')
                operation.projet_id = request.POST.get('projet')
                operation.description = request.POST.get('description')
                operation.date_debut_operation = request.POST.get('date_debut_operation')
                operation.date_fin_operation = request.POST.get('date_fin_operation') or None
                operation.duree_depot_physique = int(request.POST.get('duree_depot_physique') or 0)
                operation.duree_souscription = int(request.POST.get('duree_souscription') or 0)
                operation.montant_souscription = int(request.POST.get('montant_souscription') or 0)
                operation.disponible = request.POST.get('disponible') == 'on'
                operation.actif = 'is_active' in request.POST

                # Mise à jour du visuel
                if request.FILES.get('visuel'):
                    operation.visuel = request.FILES['visuel']

                # Mise à jour des relations many-to-many avec les IDs
                if request.POST.getlist('types_souscripteurs'):
                    operation.types_souscripteurs.set(request.POST.getlist('types_souscripteurs'))
                if request.POST.getlist('types_parcelles'):
                    operation.types_parcelles.set(request.POST.getlist('types_parcelles'))
                if request.POST.getlist('processus_attributions'):
                    operation.processus_attributions.set(request.POST.getlist('processus_attributions'))
                if request.POST.getlist('comptes_bancaires'):
                    operation.comptes_bancaires.set(request.POST.getlist('comptes_bancaires'))

                # Mise à jour ou création de la condition
                if operation.condition:
                    condition = operation.condition
                    condition.code = request.POST.get('condition_code')
                    condition.intitule = request.POST.get('condition_intitule')
                    condition.condition_souscription = request.POST.get('condition_souscription')
                    condition.methode_attribution = request.POST.get('methode_attribution')
                    condition.documents_requis = request.POST.get('documents_requis')
                    condition.operation = operation
                    condition.actif = 'is_active' in request.POST
                    condition.save()
                elif request.POST.get('condition_code') and request.POST.get('condition_intitule'):
                    condition = Condition.objects.create(
                        code=request.POST.get('condition_code'),
                        intitule=request.POST.get('condition_intitule'),
                        condition_souscription=request.POST.get('condition_souscription', ''),
                        methode_attribution=request.POST.get('methode_attribution', ''),
                        documents_requis=request.POST.get('documents_requis', ''),
                        operation=operation,
                        actif=True
                    )
                    operation.condition = condition

                operation.save()

            messages.success(request, 'Opération modifiée avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            
    return redirect('tableau_administration:liste_operations')

@login_required(login_url='tableau_administration:connexion')
def supprimer_operation(request, operation_id):
    operation = get_object_or_404(Operations, id=operation_id)
    
    try:
        intitule = operation.intitule
        operation.delete()
        messages.success(request, f'L\'opération "{intitule}" a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        
    return redirect('tableau_administration:liste_operations')

def souscrire(request):
    operations = Operation.objects.filter(actif=True).select_related(
        'projet', 
        'projet__localite',
        'condition'
    ).prefetch_related(
        'parcelles',
        'parcelles__position',
        'parcelles__usage',
        'types_souscripteurs',
        'types_parcelles',
        'types_parcelles__caracteristiques',
        'positions_parcelles',
        'positions_parcelles__type_parcelle'
    ).values(
        'id', 
        'intitule', 
        'montant_souscription',
        'duree_souscription'
    )
    
    # Préparer les types de souscripteurs pour chaque opération
    for operation in operations:
        operation.has_physique = operation.types_souscripteurs.filter(code='PHYSIQUE').exists()
        operation.has_morale = operation.types_souscripteurs.filter(code='MORALE').exists()
    
    context = {
        'operations': operations,
    }
    return render(request, 'plateforme_web/souscrire.html', context)

class ParcelleDeblocageThread:
    _instance = None
    _thread = None
    _stop_event = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None

    def debloquer_parcelles_expirees(self):
        while not self._stop_event.is_set():
            try:
                # Fermer la connexion précédente si elle existe
                connection.close()
                
                now = timezone.now()
                parcelles_expirees = ListesParcelles.objects.filter(
                    bloquer=True,
                    date_blocage__isnull=False,
                    date_fin_blocage__lte=now,
                    paye=False
                )

                for parcelle in parcelles_expirees:
                    try:
                        parcelle.bloquer = False
                        parcelle.date_blocage = None
                        parcelle.date_fin_blocage = None
                        parcelle.save()
                        logger.info(f"Parcelle {parcelle.id} débloquée automatiquement à {now}")
                    except Exception as e:
                        logger.error(f"Erreur lors du déblocage de la parcelle {parcelle.id}: {str(e)}")

            except Exception as e:
                logger.error(f"Erreur dans le thread de déblocage: {str(e)}")
            finally:
                # Fermer la connexion après utilisation
                connection.close()
            
            # Attendre 30 secondes avant la prochaine vérification
            time.sleep(30)

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self.debloquer_parcelles_expirees, daemon=True)
            self._thread.start()
            logger.info("Thread de déblocage des parcelles démarré")

    def stop(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            logger.info("Thread de déblocage des parcelles arrêté")

# Démarrer le thread au chargement du module
deblocage_thread = ParcelleDeblocageThread.get_instance()
deblocage_thread.start()

@login_required(login_url='tableau_administration:connexion')
def bloquer_parcelle(request, parcelle_id):
    if request.method == 'POST':
        try:
            parcelle = get_object_or_404(ListesParcelles, id=parcelle_id)
            
            # Vérifier si la parcelle n'est pas déjà bloquée
            if parcelle.bloquer:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cette parcelle est déjà bloquée'
                }, status=400)

            # Vérifier que la parcelle est associée à une opération
            if not parcelle.operation:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cette parcelle n\'est associée à aucune opération'
                }, status=400)

            # Bloquer la parcelle avec la durée de l'opération
            date_fin = parcelle.bloquer_parcelle()
            
            # Vérifier que le blocage a bien été effectué
            parcelle.refresh_from_db()
            
            if not parcelle.bloquer or not parcelle.date_blocage or not parcelle.date_fin_blocage:
                raise ValueError("Le blocage n'a pas été correctement enregistré")
            
            # Logger les informations
            logger.info(f"""
                Parcelle {parcelle_id} bloquée:
                - Date de blocage: {parcelle.date_blocage}
                - Date de fin: {parcelle.date_fin_blocage}
                - Durée: {parcelle.operation.duree_souscription} minutes
                - Statut blocage: {parcelle.bloquer}
                - Opération: {parcelle.operation.code}
            """)
            
            return JsonResponse({
                'status': 'success',
                'message': f'Parcelle bloquée jusqu\'à {date_fin.strftime("%H:%M:%S")}',
                'end_time': date_fin.isoformat(),
                'date_blocage': parcelle.date_blocage.isoformat(),
                'date_fin_blocage': parcelle.date_fin_blocage.isoformat(),
                'duree_blocage': parcelle.operation.duree_souscription
            })
            
        except Exception as e:
            logger.error(f"Erreur lors du blocage de la parcelle {parcelle_id}: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur lors du blocage: {str(e)}'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    }, status=405)

@login_required(login_url='tableau_administration:connexion')
def debloquer_parcelle(request, parcelle_id):
    if request.method == 'POST':
        try:
            parcelle = get_object_or_404(ListesParcelles, id=parcelle_id)
            
            # Logger l'état avant déblocage
            logger.info(f"""
                Déblocage de la parcelle {parcelle_id}:
                - État actuel: {'bloquée' if parcelle.bloquer else 'non bloquée'}
                - Date de blocage: {parcelle.date_blocage}
                - Date de fin prévue: {parcelle.date_fin_blocage}
            """)
            
            # Débloquer la parcelle
            parcelle.bloquer = False
            parcelle.date_blocage = None
            parcelle.date_fin_blocage = None
            parcelle.save()
            
            logger.info(f"Parcelle {parcelle_id} débloquée avec succès")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Parcelle débloquée avec succès'
            })
            
        except Exception as e:
            logger.error(f"Erreur lors du déblocage de la parcelle {parcelle_id}: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    }, status=405)

@csrf_protect
@require_POST
def enregistrer_souscription_et_paiement(request, parcelle_id):
    try:
        parcelle = ListesParcelles.objects.get(id=parcelle_id)
        data = json.loads(request.body)
        print("Données reçues pour souscription:", data)

        with transaction.atomic():
            identification = data['identification']
            parcelle_data = data['parcelle']
            type_parcelle_data = data['typeParcelle']
            operation_data = data['operation']
            type_personne = identification.get('typePersonne')

            # Création du souscripteur
            if type_personne == 'physique':
                # Code existant pour personne physique...
                date_naissance_str = identification.get('date_naissance')
                date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date() if date_naissance_str else None
                
                date_expiration_str = identification.get('date_expiration')
                date_expiration = datetime.strptime(date_expiration_str, '%Y-%m-%d').date() if date_expiration_str else None
                
                date_etablissement_str = identification.get('date_etablissement')
                date_etablissement = datetime.strptime(date_etablissement_str, '%Y-%m-%d').date() if date_etablissement_str else None

                souscripteur = SouscripteurPhysique.objects.create(
                    type_souscripteur=TypeSouscripteur.get_type_physique(),
                    nom_complet=identification.get('nom_complet'),
                    email=identification.get('email'),
                    telephone=identification.get('telephone'),
                    date_naissance=date_naissance,
                    lieu_naissance=identification.get('lieu_naissance'),
                    profession=identification.get('profession'),
                    genre=identification.get('genre'),
                    document=identification.get('document'),
                    numero_piece=identification.get('numero_piece'),
                    date_expiration=date_expiration,
                    lieu_etablissement=identification.get('lieu_etablissement'),
                    date_etablissement=date_etablissement,
                    pays=identification.get('pays'),
                    region=identification.get('region'),
                    ville=identification.get('ville'),
                    adresse=identification.get('adresse')
                )
                type_souscripteur = TypeSouscripteur.get_type_physique()
            else:
                # Création du souscripteur moral avec tous les champs nécessaires
                souscripteur = SouscripteurMorale.objects.create(
                    type_souscripteur=TypeSouscripteur.get_type_moral(),
                    raison_sociale=identification.get('raison_sociale'),
                    forme_juridique=identification.get('forme_juridique'),
                    rccm=identification.get('rccm'),
                    ifu=identification.get('ifu'),
                    siege_social=identification.get('siege_social'),
                    nom_representant=identification.get('nom_representant'),
                    prenom_representant=identification.get('prenom_representant'),
                    fonction_representant=identification.get('fonction_representant'),
                    telephone=identification.get('telephone'),
                    email=identification.get('email'),
                    pays=identification.get('pays'),
                    region=identification.get('region'),
                    ville=identification.get('ville'),
                    adresse=identification.get('adresse')
                )
                type_souscripteur = TypeSouscripteur.get_type_moral()

            # Marquer la parcelle comme payée et bloquée
            parcelle.paye = True
            parcelle.bloquer = True
            parcelle.save()

            # Création de la souscription avec toutes les informations de la parcelle
            souscription = SouscriptionEffectuee.objects.create(
                # Informations de l'opération
                operation=parcelle.operation,
                numero_transaction=data['paiement']['numeroTransaction'],
                type_souscripteur=type_souscripteur,
                duree_depot_physique=parcelle.operation.duree_depot_physique,
                
                # Statut confirmé
                statut='confirme',
                
                # Informations de la parcelle
                parcelle=parcelle,
                type_parcelle=parcelle.usage,
                position=parcelle.position,
                surface=float(parcelle_data.get('surface', 0)),
                cout_unitaire=float(parcelle_data.get('coutUnitaire', 0)),
                prix_total=float(parcelle_data.get('prix', 0)),
                acompte=float(parcelle_data.get('acompte', 0)),
                reste_a_payer=float(parcelle_data.get('resteAPayer', 0)),
                section=parcelle_data.get('section', ''),
                lot=parcelle_data.get('lot', ''),
                
                # Informations de paiement
                montant_souscription=float(operation_data.get('montant_souscription', 0)),
                methode_paiement=data['paiement']['methode'],
                
                # Informations communes
                telephone=identification.get('telephone'),
                email=identification.get('email'),
                pays=identification.get('pays'),
                region=identification.get('region'),
                ville=identification.get('ville'),
                adresse=identification.get('adresse'),
                
                # Pour personne physique (null si personne morale)
                nom_complet=identification.get('nom_complet') if type_personne == 'physique' else None,
                date_naissance=date_naissance if type_personne == 'physique' else None,
                lieu_naissance=identification.get('lieu_naissance') if type_personne == 'physique' else None,
                profession=identification.get('profession') if type_personne == 'physique' else None,
                genre=identification.get('genre') if type_personne == 'physique' else None,
                document=identification.get('document') if type_personne == 'physique' else None,
                numero_piece=identification.get('numero_piece') if type_personne == 'physique' else None,
                date_expiration=date_expiration if type_personne == 'physique' else None,
                lieu_etablissement=identification.get('lieu_etablissement') if type_personne == 'physique' else None,
                date_etablissement=date_etablissement if type_personne == 'physique' else None,
                
                # Pour personne morale (null si personne physique)
                raison_sociale=identification.get('raison_sociale') if type_personne == 'morale' else None,
                forme_juridique=identification.get('forme_juridique') if type_personne == 'morale' else None,
                rccm=identification.get('rccm') if type_personne == 'morale' else None,
                ifu=identification.get('ifu') if type_personne == 'morale' else None,
                siege_social=identification.get('siege_social') if type_personne == 'morale' else None,
                nom_representant=identification.get('nom_representant') if type_personne == 'morale' else None,
                prenom_representant=identification.get('prenom_representant') if type_personne == 'morale' else None,
                fonction_representant=identification.get('fonction_representant') if type_personne == 'morale' else None
            )

            # Ajout des processus d'attribution et comptes bancaires
            if parcelle.operation.processus_attributions.exists():
                souscription.processus_attributions.set(parcelle.operation.processus_attributions.all())
            
            if parcelle.operation.comptes_bancaires.exists():
                souscription.comptes_bancaires.set(parcelle.operation.comptes_bancaires.all())

            # Créer ou récupérer le mode de paiement
            mode_paiement, created = ModePaiement.objects.get_or_create(
                code=data['paiement']['methode'],
                defaults={'nom': data['paiement']['methode'], 'actif': True}
            )

            # Création du paiement associé avec statut 'confirme'
            paiement = Paiement.objects.create(
                souscripteur_physique=souscripteur if type_personne == 'physique' else None,
                souscripteur_morale=souscripteur if type_personne == 'morale' else None,
                numero_transaction=data['paiement']['numeroTransaction'],
                mode_paiement=mode_paiement,
                montant_souscription=float(operation_data.get('montant_souscription', 0)),
                statut='confirme'  # Statut directement confirmé car le paiement est réussi
            )

            print("Paiement enregistré avec succès, ID:", paiement.id)
            print("Souscription enregistrée avec succès, ID:", souscription.id)
            print("Souscripteur enregistré avec succès, ID:", souscripteur.id)
            print("Parcelle marquée comme payée, ID:", parcelle.id)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Souscription et paiement enregistrés avec succès',
                'souscription_id': souscription.id,
                'souscripteur_id': souscripteur.id,
                'paiement_id': paiement.id
            })
            
    except Exception as e:
        print("Erreur lors de l'enregistrement de la souscription:", str(e))
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_protect
@require_POST
def marquer_parcelle_payee(request, parcelle_id):
    try:
        with transaction.atomic():
            parcelle = ListesParcelles.objects.get(id=parcelle_id)
            # Marquer la parcelle comme payée
            parcelle.paye = True
            parcelle.bloquer = True  # Maintenir le blocage car payée
            parcelle.save()

            # Mettre à jour le statut du paiement associé
            souscription = SouscriptionEffectuee.objects.filter(parcelle=parcelle).latest('id')
            if souscription:
                paiement = Paiement.objects.filter(
                    Q(souscripteur_physique=souscription.souscripteur_physique) | 
                    Q(souscripteur_morale=souscription.souscripteur_morale)
                ).latest('id')
                if paiement:
                    paiement.statut = 'confirme'
                    paiement.save()

            return JsonResponse({'status': 'success', 'message': 'Parcelle marquée comme payée'})
    except Exception as e:
        print("Erreur lors du marquage de la parcelle comme payée:", str(e))
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)



@csrf_protect
@require_POST
def debloquer_parcelle(request, parcelle_id):
    if request.method == 'POST':
        parcelle = get_object_or_404(ListesParcelles, id=parcelle_id)
        
        parcelle.bloquer = False
        parcelle.date_blocage = None
        parcelle.date_fin_blocage = None
        parcelle.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='tableau_administration:connexion')
def liste_souscriptions(request):
    search_query = request.GET.get('search', '')
    
    souscriptions = SouscriptionEffectuee.objects.select_related(
        'type_souscripteur',
        'parcelle',
        'parcelle__position',
        'parcelle__usage',
        'operation',
        'operation__projet',
        'operation__projet__localite'
    ).all().order_by('-date_souscription')
    
    if search_query:
        souscriptions = souscriptions.filter(
            Q(numero_transaction__icontains=search_query) |
            Q(nom_complet__icontains=search_query) |
            Q(raison_sociale__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(parcelle__code__icontains=search_query) |
            Q(parcelle__site__icontains=search_query) |
            Q(parcelle__zone__icontains=search_query) |
            Q(parcelle__section__icontains=search_query) |
            Q(parcelle__lot__icontains=search_query)
        )
    
    paginator = Paginator(souscriptions, 10)
    page = request.GET.get('page')
    souscriptions = paginator.get_page(page)
    
    context = {
        'souscriptions': souscriptions,
        'search_query': search_query,
    }
    
    return render(request, 'tableau_administration/liste_souscriptions.html', context)

@login_required(login_url='tableau_administration:connexion')
def souscription_details(request, souscription_id):
    souscription = get_object_or_404(SouscriptionEffectuee, id=souscription_id)
    
    data = {
        'numero_transaction': souscription.numero_transaction,
        'date_souscription': souscription.date_souscription.strftime('%d/%m/%Y'),
        'montant_souscription': f"{int(souscription.montant_souscription):,}".replace(',', ' '),
        'statut': souscription.statut,
        
        'type_souscripteur': str(souscription.type_souscripteur),
        'nom_souscripteur': souscription.nom_complet if souscription.type_souscripteur.code == 'PHYSIQUE' else souscription.raison_sociale,
        'telephone': souscription.telephone,
        'email': souscription.email,
        
        'reference_parcelle': souscription.parcelle.reference,
        'type_parcelle': str(souscription.type_parcelle),
        'surface': f"{int(souscription.surface):,}".replace(',', ' '),
        'prix_total': f"{int(souscription.prix_total):,}".replace(',', ' '),
        
        'projet': str(souscription.operation),
        'localite': str(souscription.operation.localite) if souscription.operation else 'Non spécifié'
    }
    
    return JsonResponse(data)

@login_required(login_url='tableau_administration:connexion')
def modifier_souscription(request, souscription_id):
    souscription = get_object_or_404(SouscriptionEffectuee, id=souscription_id)
    
    if request.method == 'POST':
        try:
            # Mettre à jour les champs de la souscription
            souscription.statut = request.POST.get('statut', '') == 'on'
            souscription.save()
            
            messages.success(request, 'La souscription a été modifiée avec succès.')
            return redirect('tableau_administration:liste_souscriptions')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification de la souscription : {str(e)}')
    
    context = {
        'souscription': souscription
    }
    return render(request, 'tableau_administration/modifier_souscription.html', context)

@login_required(login_url='tableau_administration:connexion')
def supprimer_souscription(request, souscription_id):
    souscription = get_object_or_404(SouscriptionEffectuee, id=souscription_id)
    
    try:
        souscription.delete()
        messages.success(request, 'La souscription a été supprimée avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression de la souscription : {str(e)}')
    
    return redirect('tableau_administration:liste_souscriptions')


def liste_paiements(request):
    search_query = request.GET.get('search', '')
    paiements = Paiement.objects.all().order_by('-date_paiement')
    
    # Calcul des totaux
    total_montant = paiements.aggregate(total=Sum('montant_souscription'))['total'] or 0
    total_confirmes = paiements.filter(statut='confirme').aggregate(total=Sum('montant_souscription'))['total'] or 0
    total_en_attente = paiements.filter(statut='en_attente').aggregate(total=Sum('montant_souscription'))['total'] or 0
    
    if search_query:
        paiements = paiements.filter(
            Q(numero_transaction__icontains=search_query) |
            Q(souscripteur_physique__nom_complet__icontains=search_query) |
            Q(souscripteur_morale__raison_sociale__icontains=search_query) 
        )


    paginator = Paginator(paiements, 10)
    page = request.GET.get('page')
    paiements = paginator.get_page(page)

    context = {
        'paiements': paiements,
        'search_query': search_query,
        'total_montant': total_montant,
        'total_confirmes': total_confirmes,
        'total_en_attente': total_en_attente,
    }
    
    return render(request, 'tableau_administration/liste_paiements.html', context)

@login_required(login_url='tableau_administration:connexion')
def paiement_details(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    souscription = paiement.souscription
    
    data = {
        'numero_transaction': paiement.numero_transaction,
        'date_paiement': paiement.date_paiement.strftime('%d/%m/%Y'),
        'montant': f"{int(paiement.montant):,}".replace(',', ' '),
        'methode_paiement': str(paiement.methode_paiement),
        
        'type_souscripteur': str(souscription.type_souscripteur),
        'nom_souscripteur': souscription.nom_complet if souscription.type_souscripteur.code == 'PHYSIQUE' else souscription.raison_sociale,
        'telephone': souscription.telephone,
        'email': souscription.email,
        
        'reference_parcelle': souscription.parcelle.reference,
        'type_parcelle': str(souscription.type_parcelle),
        'surface': f"{int(souscription.surface):,}".replace(',', ' '),
        'prix_total': f"{int(souscription.prix_total):,}".replace(',', ' '),
        
        'banque': paiement.compte_bancaire.nom if paiement.compte_bancaire else 'Non spécifié',
        'compte': paiement.compte_bancaire.numero_compte if paiement.compte_bancaire else 'Non spécifié'
    }
    
    return JsonResponse(data)

@login_required(login_url='tableau_administration:connexion')
def ajouter_paiement(request):
    if request.method == 'POST':
        try:
            souscription_id = request.POST.get('souscription')
            souscription = get_object_or_404(SouscriptionEffectuee, id=souscription_id)
            
            paiement = Paiement(
                souscription=souscription,
                montant=request.POST.get('montant'),
                methode_paiement_id=request.POST.get('methode_paiement'),
                compte_bancaire_id=request.POST.get('compte_bancaire'),
                numero_transaction=request.POST.get('numero_transaction')
            )
            paiement.save()
            
            # Mettre à jour le statut de la souscription
            souscription.statut = True
            souscription.save()
            
            messages.success(request, 'Le paiement a été ajouté avec succès.')
            return redirect('tableau_administration:liste_paiements')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout du paiement : {str(e)}')
    
    context = {
        'souscriptions': SouscriptionEffectuee.objects.filter(statut=False),
        'methodes_paiement': ModePaiement.objects.filter(actif=True),
        'comptes_bancaires': CompteBancaire.objects.filter(actif=True)
    }
    return render(request, 'tableau_administration/ajouter_paiement.html', context)

@login_required(login_url='tableau_administration:connexion')
def modifier_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    
    if request.method == 'POST':
        try:
            paiement.montant = request.POST.get('montant')
            paiement.methode_paiement_id = request.POST.get('methode_paiement')
            paiement.compte_bancaire_id = request.POST.get('compte_bancaire')
            paiement.save()
            
            messages.success(request, 'Le paiement a été modifié avec succès.')
            return redirect('tableau_administration:liste_paiements')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification du paiement : {str(e)}')
    
    context = {
        'paiement': paiement,
        'methodes_paiement': ModePaiement.objects.filter(actif=True),
        'comptes_bancaires': CompteBancaire.objects.filter(actif=True)
    }
    return render(request, 'tableau_administration/modifier_paiement.html', context)

@login_required(login_url='tableau_administration:connexion')
def supprimer_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    
    try:
        # Mettre à jour le statut de la souscription
        souscription = paiement.souscription
        souscription.statut = False
        souscription.save()
        
        paiement.delete()
        messages.success(request, 'Le paiement a été supprimé avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression du paiement : {str(e)}')
    
    return redirect('tableau_administration:liste_paiements')

def initier_paiement(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Données reçues: {data}")
            
            # Configuration de l'API LigdiCash
            api_key = settings.LIGDICASH_API_KEY
            api_token = settings.LIGDICASH_API_TOKEN
            
            # Calcul du montant total
            montant = int(data['operation']['montant_souscription'])
            
            # Préparation des données client
            if data['identification'].get('typePersonne') == 'physique':
                nom_complet = data['identification'].get('nom_complet', '').split()
                prenom = nom_complet[0] if nom_complet else ''
                nom = ' '.join(nom_complet[1:]) if len(nom_complet) > 1 else ''
            else:
                prenom = data['identification'].get('nom_representant', '')
                nom = data['identification'].get('prenom_representant', '')
            
            # Construction des URLs absolues
            base_url = request.build_absolute_uri('/').rstrip('/')
            
            # Préparer les données pour LigdiCash
            payload = {
                "commande": {
                    "invoice": {
                        "items": [
                            {
                                "name": "Souscription parcelle SONATUR",
                                "description": f"Souscription parcelle {data['parcelle']['code']}",
                                "quantity": 1,
                                "unit_price": montant,
                                "total_price": montant
                            }
                        ],
                        "total_amount": montant,
                        "devise": "XOF",
                        "description": f"Paiement souscription parcelle {data['parcelle']['code']} - SONATUR",
                        "customer": "",
                        "customer_firstname": prenom,
                        "customer_lastname": nom,
                        "customer_email": data['identification'].get('email', ''),
                        "external_id": "",
                        "otp": ""
                    },
                    "store": {
                        "name": "SONATUR",
                        "website_url": base_url
                    },
                    "actions": {
                        "cancel_url": f"{base_url}/souscrire",
                        "return_url": f"{base_url}/souscrire?step=7&payment=success",
                        "callback_url": f"{base_url}/api/paiement/callback/"
                    },
                    "custom_data": {
                        "transaction_id": data['paiement']['numeroTransaction']
                    }
                }
            }

            # Appel à l'API LigdiCash
            headers = {
                'Apikey': api_key,
                'Authorization': f'Bearer {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create',
                json=payload,
                headers=headers
            )
            
            response_data = response.json()
            
            if response_data.get('response_code') == '00':
                return JsonResponse({
                    'status': 'success',
                    'payment_url': response_data.get('response_text'),
                    'token': response_data.get('token')
                })
            else:
                error_message = response_data.get('response_text', 'Erreur inconnue')
                logger.error(f"Erreur LigdiCash: {error_message}")
                return JsonResponse({
                    'status': 'error',
                    'message': f"Erreur LigdiCash: {error_message}"
                }, status=400)
                
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Une erreur est survenue: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée'
    }, status=405)

def verifier_paiement(request, token):
    try:
        # Configuration de l'API LigdiCash
        api_key = settings.LIGDICASH_API_KEY
        api_token = settings.LIGDICASH_API_TOKEN
        
        # Appel à l'API LigdiCash pour vérifier le statut
        headers = {
            'Apikey': api_key,
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/?invoiceToken={token}',
            headers=headers
        )
        
        response_data = response.json()
        
        if response_data['response_code'] == '00' and response_data['status'] == 'completed':
            return JsonResponse({
                'status': 'success',
                'payment_status': 'completed'
            })
        else:
            return JsonResponse({
                'status': 'pending',
                'payment_status': response_data['status']
            })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt  # Exemption CSRF pour les callbacks API externes
def callback_paiement(request):
    try:
        data = json.loads(request.body)
        numero_transaction = data.get('transaction_id')
        statut_paiement = data.get('status')
        
        with transaction.atomic():
            # Rechercher le paiement par numéro de transaction
            paiement = Paiement.objects.get(numero_transaction=numero_transaction)
            
            if statut_paiement == 'success':
                # Mettre à jour le statut du paiement
                paiement.statut = 'confirme'  # Utiliser 'confirme' au lieu de 'valide' pour être cohérent
                paiement.save()
                
                # Trouver la souscription associée
                souscription = SouscriptionEffectuee.objects.get(numero_transaction=numero_transaction)
                if souscription:
                    # Marquer la parcelle comme payée
                    parcelle = souscription.parcelle
                    parcelle.paye = True
                    parcelle.bloquer = True
                    parcelle.save()
                    print(f"Parcelle {parcelle.id} marquée comme payée dans callback_paiement")
                    
                return JsonResponse({
                    'status': 'success',
                    'message': 'Paiement validé avec succès'
                })
                
            elif statut_paiement in ['failed', 'cancelled', 'expired']:
                # Mettre à jour le statut du paiement
                paiement.statut = 'annule'
                paiement.save()
                
                # Trouver la souscription associée
                souscription = SouscriptionEffectuee.objects.get(numero_transaction=numero_transaction)
                if souscription:
                    # Débloquer la parcelle
                    parcelle = souscription.parcelle
                    parcelle.bloquer = False
                    parcelle.paye = False
                    parcelle.save()
                    print(f"Parcelle {parcelle.id} débloquée dans callback_paiement")
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Paiement marqué comme annulé'
                })
            
            return JsonResponse({
                'status': 'success',
                'message': 'Statut de paiement mis à jour'
            })
            
    except Exception as e:
        print("Erreur lors du traitement du callback de paiement:", str(e))
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def debloquer_parcelles_expirees():
    """Fonction pour débloquer automatiquement les parcelles dont le temps est expiré"""
    parcelles_bloquees = ListesParcelles.objects.filter(
        bloquer=True,
        date_blocage__isnull=False,
        date_fin_blocage__lte=timezone.now()
    )
    
    for parcelle in parcelles_bloquees:
        parcelle.bloquer = False
        parcelle.date_blocage = None
        parcelle.date_fin_blocage = None
        parcelle.save()