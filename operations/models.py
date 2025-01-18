from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from paiements.models import CompteBancaire
from souscriptions.models import TypeSouscripteur
from datetime import timedelta

class Operations(models.Model):
    code = models.CharField(
        verbose_name=_("Code"), 
        max_length=50
    )
    intitule = models.CharField(
        verbose_name=_("Intitulé"), 
        max_length=200
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True
    )
    date_debut_operation = models.DateTimeField(
        verbose_name=_("Date et heure de début de l'opération"),
        default=timezone.now
    )
    date_fin_operation = models.DateTimeField(
        verbose_name=_("Date et heure de fin de l'opération"),
        blank=True,
        null=True
    )
    duree_depot_physique = models.PositiveIntegerField(
        verbose_name=_("Durée pour le dépôt physique (en jours)"),
        default=0
    )
    duree_souscription = models.PositiveIntegerField(
        verbose_name=_("Durée d'une souscription (en minutes)"),
        default=0
    )
    montant_souscription = models.PositiveIntegerField(
        verbose_name=_("Montant de la souscription (FCFA)"),
        default=0
    )
    types_souscripteurs = models.ManyToManyField(
        TypeSouscripteur,
        verbose_name=_("Types de souscripteur"),
        related_name='operations'
    )
    types_parcelles = models.ManyToManyField(
        'TypeParcelle',
        verbose_name=_("Types de parcelles"),
        related_name='operations'
    )
    processus_attributions = models.ManyToManyField(
        'ProcessusAttribution',
        verbose_name=_("Processus d'attribution des parcelles"),
        related_name='operations_processus'
    )
    projet = models.ForeignKey(
        'Projet',
        on_delete=models.CASCADE,
        verbose_name=_("Projet"),
        related_name='operations'
    )
    comptes_bancaires = models.ManyToManyField(
        CompteBancaire,
        verbose_name=_("Comptes bancaires"),
        related_name='operations'
    )
    visuel = models.ImageField(upload_to='operations/visuels/', null=True, blank=True)
    disponible = models.BooleanField(
        verbose_name=_("Rendre disponible"),
        default=False
    )
    condition = models.ForeignKey(
        'Condition',
        on_delete=models.SET_NULL,
        verbose_name=_("Condition"),
        related_name='operations',
        null=True,
        blank=True
    )
    parcelles = models.ManyToManyField(
        'ListesParcelles', blank=True,
        verbose_name=_("Parcelles"),
        related_name='operations_liste'
    )

    positions_parcelles = models.ManyToManyField(
        'PositionParcelle', blank=True,
        verbose_name=_("Positions de parcelles"),
        related_name='operations_positions'
    )
    actif = models.BooleanField(
        verbose_name=_("Actif"),
        default=True
    )

    class Meta:
        verbose_name = _("Opération")
        verbose_name_plural = _("Opérations")
        ordering = ['-date_debut_operation']

    def __str__(self):
        return f"{self.intitule} ({self.code})"


class TypeParcelle(models.Model):
    code = models.CharField(
        verbose_name=_("Code du type de parcelle"), 
        max_length=50
    )
    nom = models.CharField(
        verbose_name=_("Nom du type de parcelle"), 
        max_length=200
    )
    description = models.TextField(
        verbose_name=_("Description du type de parcelle"), 
        blank=True, 
        null=True
    )
    actif = models.BooleanField(
        verbose_name=_("Type de parcelle actif"), 
        default=True
    )

    class Meta:
        verbose_name = _("Type de parcelle")
        verbose_name_plural = _("Types de parcelles")
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Localite(models.Model):
    code = models.CharField(
        verbose_name=_("Code de la localité"), 
        max_length=50
    )
    nom = models.CharField(
        verbose_name=_("Nom de la localité"), 
        max_length=200
    )
    description = models.TextField(
        verbose_name=_("Description de la localité"), 
        blank=True, 
        null=True
    )
    actif = models.BooleanField(
        verbose_name=_("Localité active"), 
        default=True
    )

    class Meta:
        verbose_name = _("Localité")
        verbose_name_plural = _("Localités")
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Projet(models.Model):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    localite = models.ForeignKey('Localite', on_delete=models.CASCADE)
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    superficie_origine = models.FloatField(default=0)
    superficie_viabilisee = models.FloatField(default=0)
    actif = models.BooleanField(default=True)
    date_archivage = models.DateTimeField(blank=True, null=True, editable=False)  # Champ en lecture seule
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        # Si le projet est archivé et que la date d'archivage n'est pas encore définie
        if self.archive and not self.date_archivage:
            self.date_archivage = timezone.now()
        # Si le projet n'est plus archivé, réinitialiser la date d'archivage
        elif not self.archive:
            self.date_archivage = None
        super().save(*args, **kwargs)
    
class ProcessusAttribution(models.Model):
    code = models.CharField(
        verbose_name=_("Code du processus d'attribution"), 
        max_length=50
    )
    nom = models.CharField(
        verbose_name=_("Nom du processus d'attribution"), 
        max_length=200
    )
    description = models.TextField(
        verbose_name=_("Description du processus d'attribution"), 
        blank=True, 
        null=True
    )

    date_creation = models.DateTimeField(
        verbose_name=_("Date de création"),
        auto_now_add=True
    )
    actif = models.BooleanField(
        verbose_name=_("Processus d'attribution actif"), 
        default=True
    )

    class Meta:
        verbose_name = _("Processus d'attribution")
        verbose_name_plural = _("Processus d'attribution")
        ordering = ['nom']

    def __str__(self):
        return self.nom

class PositionParcelle(models.Model):
    code = models.CharField(
        verbose_name=_("Code de la position de parcelle"), 
        max_length=50
    )
    nom = models.CharField(
        verbose_name=_("Nom de la position de parcelle"), 
        max_length=200
    )
    description = models.TextField(
        verbose_name=_("Description de la position de parcelle"), 
        blank=True, 
        null=True
    )
    type_parcelle = models.ForeignKey(
        TypeParcelle, 
        on_delete=models.CASCADE,
        verbose_name=_("Type de parcelle"),
        related_name='positions_parcelles'
    )
    actif = models.BooleanField(
        verbose_name=_("Position de parcelle active"), 
        default=True
    )

    class Meta:
        verbose_name = _("Position de parcelle")
        verbose_name_plural = _("Positions de parcelles")
        ordering = ['nom']

    def __str__(self):
        return self.nom

class ListesParcelles(models.Model):
    operation = models.ForeignKey(
        Operations,
        on_delete=models.CASCADE,
        verbose_name=_("Opération"),
        related_name='parcelles_operation',
        null=True,
        blank=True
    )
    code = models.CharField(
        verbose_name=_("Code de la parcelle"),
        max_length=100
    )
    site = models.CharField(
        verbose_name=_("Site"),
        max_length=100
    )
    zone = models.CharField(
        verbose_name=_("Zone"),
        max_length=100
    )
    section = models.CharField(
        verbose_name=_("Section"),
        max_length=100
    )
    position = models.ForeignKey(
        PositionParcelle,
        on_delete=models.CASCADE,
        verbose_name=_("Position de parcelle"),
        related_name='parcelles_position',
        null=True,
        blank=True
    )
    lot = models.CharField(
        verbose_name=_("Lot"),
        max_length=100
    )
    parcelle = models.CharField(
        verbose_name=_("Parcelle"),
        max_length=100
    )
    usage = models.ForeignKey(
        TypeParcelle,
        on_delete=models.CASCADE,
        verbose_name=_("Type de parcelle"),
        related_name='parcelles_type',
        null=True,
        blank=True
    )
    surface = models.IntegerField(
        verbose_name=_("Surface")
    )
    cout_m2 = models.IntegerField(
        verbose_name=_("Coût au m²")
    )
    acompte = models.IntegerField(
        verbose_name=_("Acompte")
    )
    reste_a_payer = models.IntegerField(
        verbose_name=_("Reste à payer"),
        editable=True
    )
    cout_total = models.IntegerField(
        verbose_name=_("Coût total"),
        editable=True
    )
    paye = models.BooleanField(
        verbose_name=_("Payé"),
        default=False
    )
    actif = models.BooleanField(
        verbose_name=_("Actif"),
        default=True
    )
    bloquer = models.BooleanField(
        verbose_name=_("Bloqué"),
        default=False
    )
    date_blocage = models.DateTimeField(
        verbose_name=_("Date de blocage"),
        null=True, 
        blank=True
    )
    date_fin_blocage = models.DateTimeField(
        verbose_name=_("Date de fin de blocage"),
        null=True, 
        blank=True
    )
  
    date_ajout = models.DateTimeField(
        verbose_name=_("Date d'ajout"),
        default=timezone.now
    )

    def bloquer_parcelle(self):
        """Méthode pour bloquer une parcelle avec la durée de souscription de l'opération"""
        now = timezone.now()
        # Récupérer la durée de souscription de l'opération (en minutes)
        duree_minutes = self.operation.duree_souscription if self.operation else 20

        self.bloquer = True
        self.date_blocage = now
        self.date_fin_blocage = now + timedelta(minutes=duree_minutes)
        self.save(update_fields=['bloquer', 'date_blocage', 'date_fin_blocage'])
        return self.date_fin_blocage

    def save(self, *args, **kwargs):
        if not self.cout_total:
            self.cout_total = self.surface * self.cout_m2
        if not self.reste_a_payer:
            self.reste_a_payer = self.cout_total - self.acompte
            
        # Vérification explicite des dates de blocage
        if self.bloquer and not self.date_blocage:
            self.date_blocage = timezone.now()
        if self.bloquer and not self.date_fin_blocage and self.operation:
            self.date_fin_blocage = self.date_blocage + timedelta(minutes=self.operation.duree_souscription)
            
        # Logique de déblocage automatique
        if self.bloquer and self.date_fin_blocage and timezone.now() >= self.date_fin_blocage:
            self.bloquer = False
            self.date_blocage = None
            self.date_fin_blocage = None
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.site} - {self.zone} - {self.parcelle}"

    class Meta:
        verbose_name = _("Liste des Parcelles")
        verbose_name_plural = _("Listes des Parcelles")
        ordering = ['site', 'zone', 'parcelle', '-date_ajout']

class Condition(models.Model):
    code = models.CharField(
        verbose_name=_("Code de la condition"), 
        max_length=50,
        unique=True
    )
    intitule = models.CharField(
        verbose_name=_("Intitulé de la condition"), 
        max_length=200
    )
    condition_souscription = models.TextField(
        verbose_name=_("Conditions de souscription"),
        help_text=_("Décrivez les conditions requises pour la souscription")
    )
    methode_attribution = models.TextField(
        verbose_name=_("Description de la méthode d'attribution"),
        help_text=_("Décrivez la méthode utilisée pour l'attribution")
    )
    documents_requis = models.TextField(
        verbose_name=_("Description des documents à fournir"),
        help_text=_("Listez tous les documents nécessaires")
    )
    operation = models.ForeignKey(
        Operations, null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Opération"),
        related_name='conditions' 
    )
    date_creation = models.DateTimeField(
        verbose_name=_("Date de création"),
        auto_now_add=True
    )
    date_modification = models.DateTimeField(
        verbose_name=_("Dernière modification"),
        auto_now=True
    )
    actif = models.BooleanField(
        verbose_name=_("Condition active"),
        default=True
    )

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.code} - {self.intitule}"

    def save(self, *args, **kwargs):
        # Convertir le code en majuscules avant la sauvegarde
        self.code = self.code.upper()
        super().save(*args, **kwargs)

class Parcelle(models.Model):
    cout_m2 = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True,  # Permet des valeurs NULL
        blank=True, # Permet des valeurs vides dans les formulaires
        default=0
    )

