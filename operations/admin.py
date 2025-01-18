from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import (
    TypeParcelle, PositionParcelle, Localite, Projet, 
    ProcessusAttribution, Operations, ListesParcelles, Condition
)

@admin.register(TypeParcelle)
class TypeParcelleAdmin(ImportExportModelAdmin):
    list_display = ('code', 'nom', 'description', 'actif')
    search_fields = ('code', 'nom', 'description')
    list_filter = ('actif',)

@admin.register(PositionParcelle)
class PositionParcelleAdmin(ImportExportModelAdmin):
    list_display = ('code', 'nom', 'type_parcelle', 'description', 'actif')
    search_fields = ('code', 'nom', 'description')
    list_filter = ('actif', 'type_parcelle')

@admin.register(Localite)
class LocaliteAdmin(ImportExportModelAdmin):
    list_display = ('code', 'nom', 'description', 'actif')
    search_fields = ('code', 'nom', 'description')
    list_filter = ('actif',)



@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    # Champs à afficher dans la liste des projets
    list_display = (
        'code', 
        'libelle', 
        'date_debut', 
        'date_fin', 
        'localite', 
        'actif', 
        'archive', 
        'date_archivage'  # Ajout du champ date_archivage
    )
    
    # Champs utilisés pour la recherche
    search_fields = (
        'code', 
        'libelle', 
        'description'
    )
    
    # Filtres disponibles dans la liste
    list_filter = (
        'actif', 
        'archive', 
        'localite', 
        'date_debut', 
        'date_fin'
    )
    
    # Champs en lecture seule dans le formulaire d'édition
    readonly_fields = (
        'date_creation', 
        'date_archivage'  # Ajout du champ date_archivage en lecture seule
    )
@admin.register(ProcessusAttribution)
class ProcessusAttributionAdmin(ImportExportModelAdmin):
    list_display = ('code', 'nom', 'description', 'actif')
    search_fields = ('code', 'nom', 'description')
    list_filter = ('actif',)

@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'intitule', 'projet', 'date_debut_operation',
        'date_fin_operation', 'disponible', 'description', 'get_positions'
    )
    list_filter = ('disponible', 'projet', 'date_debut_operation')
    search_fields = ('code', 'intitule', 'projet__libelle')
    filter_horizontal = (
        'types_souscripteurs', 'types_parcelles',
        'processus_attributions', 'comptes_bancaires', 'parcelles',
        'positions_parcelles'
    )
    fieldsets = (
        (_('Informations générales'), {
            'fields': (
                'code', 'intitule', 'projet', 'disponible',
                'visuel', 'condition', 'description'
            )
        }),
        (_('Dates et durées'), {
            'fields': (
                'date_debut_operation', 'date_fin_operation',
                'duree_depot_physique', 'duree_souscription'
            )
        }),
        (_('Paramètres financiers'), {
            'fields': ('montant_souscription', 'comptes_bancaires')
        }),
        (_('Relations'), {
            'fields': (
                'types_souscripteurs', 'types_parcelles',
                'processus_attributions', 'parcelles', 'positions_parcelles'
            )
        }),
    )

    def get_positions(self, obj):
        return ", ".join([p.nom for p in obj.positions_parcelles.all()[:3]])
    get_positions.short_description = "Positions"


@admin.register(ListesParcelles)
class ListesParcellesAdmin(ImportExportModelAdmin):
    list_display = ('operation', 'site', 'zone', 'section', 'position', 'lot', 'parcelle',
                   'usage', 'surface', 'cout_m2', 'cout_total', 'acompte',
                   'reste_a_payer', 'paye', 'actif', 'bloquer', 'date_ajout')
    list_filter = ('site', 'zone', 'usage', 'paye', 'actif', 'bloquer')
    search_fields = ('site', 'zone', 'section', 'lot', 'parcelle')
    readonly_fields = ('cout_total', 'reste_a_payer', 'date_ajout')

    fieldsets = (
        (None, {
            'fields': ('operation', 'site', 'zone', 'section', 'position', 'lot', 'parcelle')
        }),
        (_('Caractéristiques'), {
            'fields': ('usage', 'surface', 'cout_m2')
        }),
        (_('Informations financières'), {
            'fields': ('cout_total', 'acompte', 'reste_a_payer', 'paye')
        }),
        (_('État'), {
            'fields': ('actif', 'bloquer', 'date_ajout', 'date_blocage', 'date_fin_blocage')
        })
    )

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('code', 'intitule', 'operation', 'actif', 'date_creation')
    list_filter = ('actif', 'operation')
    search_fields = ('code', 'intitule', 'condition_souscription')
    ordering = ('-date_creation',)
    readonly_fields = ('date_creation', 'date_modification')