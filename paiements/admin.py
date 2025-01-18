from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from django.contrib import admin
from .models import CompteBancaire, ModePaiement, Paiement

# CompteBancaire
class CompteBancaireResource(resources.ModelResource):
    class Meta:
        model = CompteBancaire

@admin.register(CompteBancaire)
class CompteBancaireAdmin(ImportExportModelAdmin):
    resource_class = CompteBancaireResource
    list_display = ('nom', 'code', 'code_banque', 'numero_compte', 'actif')
    list_filter = ('actif', 'code_banque')
    search_fields = ('nom', 'code', 'numero_compte', 'rib')
    list_editable = ('actif',)

    fieldsets = (
        (None, {
            'fields': ('code', 'nom', 'description')
        }),
        ('Détails Bancaires', {
            'fields': ('code_banque', 'code_guichet', 'numero_compte', 'rib')
        }),
        ('Informations Supplémentaires', {
            'fields': ('image', 'actif')
        })
    )


class ModePaiementResource(resources.ModelResource):
    class Meta:
        model = ModePaiement

class PaiementResource(resources.ModelResource):
    class Meta:
        model = Paiement


@admin.register(ModePaiement)
class ModePaiementAdmin(ImportExportModelAdmin):
    resource_class = ModePaiementResource
    list_display = ('code', 'nom', 'actif')
    search_fields = ('code', 'nom')
    list_filter = ('actif',)

@admin.register(Paiement)
class PaiementAdmin(ImportExportModelAdmin):
    resource_class = PaiementResource
    list_display = ('numero_transaction', 'get_souscripteur', 'date_paiement', 'montant_souscription', 'mode_paiement', 'statut')
    search_fields = ('numero_transaction',)
    list_filter = ('statut', 'date_paiement', 'mode_paiement')
    readonly_fields = ('date_paiement',)
    
    def get_souscripteur(self, obj):
        return obj.souscripteur_physique or obj.souscripteur_morale
    get_souscripteur.short_description = 'Souscripteur'
    
    fieldsets = (
        ('Informations de Base', {
            'fields': ('numero_transaction', 'montant_souscription', 'mode_paiement', 'statut')
        }),
        ('Souscripteur', {
            'fields': ('souscripteur_physique', 'souscripteur_morale')
        }),
        ('Dates', {
            'fields': ('date_paiement',)
        })
    )