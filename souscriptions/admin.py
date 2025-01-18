from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import TypeSouscripteur, SouscripteurPhysique, SouscripteurMorale, SouscriptionEffectuee

# TypeSouscripteur
class TypeSouscripteurResource(resources.ModelResource):
    class Meta:
        model = TypeSouscripteur

@admin.register(TypeSouscripteur)
class TypeSouscripteurAdmin(ImportExportModelAdmin):
    resource_class = TypeSouscripteurResource
    list_display = ('code', 'nom', 'actif', 'date_creation')
    list_filter = ('actif',)
    search_fields = ('code', 'nom')
    ordering = ('code',)

# SouscripteurPhysique
class SouscripteurPhysiqueResource(resources.ModelResource):
    class Meta:
        model = SouscripteurPhysique

@admin.register(SouscripteurPhysique)
class SouscripteurPhysiqueAdmin(ImportExportModelAdmin):
    resource_class = SouscripteurPhysiqueResource
    list_display = ('nom_complet', 'email', 'telephone', 'profession', 'actif', 'date_creation')
    list_filter = ('actif', 'genre', 'type_souscripteur')
    search_fields = ('nom_complet', 'email', 'telephone', 'numero_piece')
    ordering = ('-date_creation',)
    fieldsets = (
        ('Informations Personnelles', {
            'fields': (
                'type_souscripteur', 'nom_complet', 'email', 'telephone', 
                'date_naissance', 'lieu_naissance', 'profession', 'genre'
            )
        }),
        ('Documents d\'Identité', {
            'fields': (
                'document', 'numero_piece', 'date_expiration',
                'lieu_etablissement', 'date_etablissement'
            )
        }),
        ('Adresse', {
            'fields': ('pays', 'region', 'ville', 'adresse')
        }),
        ('Statut', {
            'fields': ('actif',)
        })
    )

# SouscripteurMorale
class SouscripteurMoraleResource(resources.ModelResource):
    class Meta:
        model = SouscripteurMorale

@admin.register(SouscripteurMorale)
class SouscripteurMoraleAdmin(ImportExportModelAdmin):
    resource_class = SouscripteurMoraleResource
    list_display = ('raison_sociale', 'forme_juridique', 'rccm', 'ifu', 'email', 'actif', 'date_creation')
    list_filter = ('actif', 'forme_juridique', 'type_souscripteur')
    search_fields = ('raison_sociale', 'rccm', 'ifu', 'email', 'nom_representant')
    ordering = ('-date_creation',)
    fieldsets = (
        ('Informations de l\'Entreprise', {
            'fields': (
                'type_souscripteur', 'raison_sociale', 'forme_juridique',
                'rccm', 'ifu', 'siege_social'
            )
        }),
        ('Représentant Légal', {
            'fields': (
                'nom_representant', 'prenom_representant', 'fonction_representant'
            )
        }),
        ('Contact', {
            'fields': ('telephone', 'email')
        }),
        ('Adresse', {
            'fields': ('pays', 'region', 'ville', 'adresse')
        }),
        ('Statut', {
            'fields': ('actif',)
        })
    )

# SouscriptionEffectuee
class SouscriptionEffectueeResource(resources.ModelResource):
    class Meta:
        model = SouscriptionEffectuee

@admin.register(SouscriptionEffectuee)
class SouscriptionEffectueeAdmin(ImportExportModelAdmin):
    resource_class = SouscriptionEffectueeResource
    list_display = ('numero_transaction', 'get_souscripteur', 'operation', 'date_souscription', 'duree_depot_physique', 'montant_souscription', 'methode_paiement')
    list_filter = ('operation', 'date_souscription', 'type_souscripteur', 'methode_paiement')
    search_fields = ('numero_transaction', 'nom_complet', 'raison_sociale', 'email', 'telephone')
    readonly_fields = ('date_souscription', 'date_paiement')
    filter_horizontal = ('processus_attributions', 'comptes_bancaires')

    def get_souscripteur(self, obj):
        if obj.type_souscripteur.code == 'PHYSIQUE':
            return obj.nom_complet
        return obj.raison_sociale
    get_souscripteur.short_description = 'Souscripteur'

    fieldsets = (
        ('Informations de l\'opération', {
            'fields': ('operation', 'numero_transaction', 'date_souscription', 'duree_depot_physique', 'processus_attributions', 'comptes_bancaires')
        }),
        ('Informations du souscripteur', {
            'fields': ('type_souscripteur', ('nom_complet', 'raison_sociale'), 'telephone', 'email')
        }),
        ('Informations de la parcelle', {
            'fields': ('parcelle', 'type_parcelle', 'position', 'surface', 'cout_unitaire', 'prix_total', 'acompte', 'reste_a_payer', 'section', 'lot')
        }),
        ('Informations de paiement', {
            'fields': ('montant_souscription', 'methode_paiement', 'date_paiement')
        }),
        ('Détails personne physique', {
            'classes': ('collapse',),
            'fields': ('date_naissance', 'lieu_naissance', 'profession', 'genre', 'document', 'numero_piece', 'date_expiration', 'lieu_etablissement', 'date_etablissement')
        }),
        ('Détails personne morale', {
            'classes': ('collapse',),
            'fields': ('forme_juridique', 'rccm', 'ifu', 'siege_social', 'nom_representant', 'prenom_representant', 'fonction_representant')
        }),
        ('Adresse', {
            'fields': ('pays', 'region', 'ville', 'adresse')
        })
    )