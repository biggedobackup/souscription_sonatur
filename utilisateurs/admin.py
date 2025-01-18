from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Role, Utilisateur

# Role
class RoleResource(resources.ModelResource):
    class Meta:
        model = Role

@admin.register(Role)
class RoleAdmin(ImportExportModelAdmin):
    resource_class = RoleResource
    list_display = ('nom', 'description', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    fieldsets = (
        (None, {
            'fields': ('nom', 'description')
        }),
        (_('Statut'), {
            'fields': ('actif',)
        }),
    )

# Utilisateur
class UtilisateurResource(resources.ModelResource):
    class Meta:
        model = Utilisateur
        exclude = ('password',)

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = UtilisateurResource
    list_display = ('email', 'nom_complet', 'role', 'actif', 'date_creation')
    list_filter = ('actif', 'role', 'date_creation')
    search_fields = ('email', 'nom_complet')
    ordering = ('-date_creation',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Informations personnelles'), {
            'fields': ('nom_complet', 'role')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Dates importantes'), {
            'fields': ('last_login', 'date_creation')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom_complet', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ('date_creation',)
    filter_horizontal = ('groups', 'user_permissions',)