from django.db import models
from django.utils.translation import gettext_lazy as _
from souscriptions.models import SouscripteurPhysique, SouscripteurMorale

class CompteBancaire(models.Model):
    code = models.CharField(
        max_length=50, 
        verbose_name=_("Code du compte"),
        help_text=_("Code unique identifiant le compte bancaire")
    )
    nom = models.CharField(
        max_length=200, 
        verbose_name=_("Nom du compte"),
        help_text=_("Nom descriptif du compte bancaire")
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Description"),
        help_text=_("Description détaillée du compte bancaire")
    )
    code_banque = models.CharField(
        max_length=50, 
        verbose_name=_("Code banque"),
        help_text=_("Code d'identification de la banque")
    )
    code_guichet = models.CharField(
        max_length=50, 
        verbose_name=_("Code guichet"),
        help_text=_("Code du guichet bancaire")
    )
    numero_compte = models.CharField(
        max_length=50, 
        verbose_name=_("Numéro de compte"),
        help_text=_("Numéro unique du compte bancaire")
    )
    rib = models.CharField(
        max_length=100, 
        verbose_name=_("RIB"),
        help_text=_("Relevé d'Identité Bancaire complet")
    )
    image = models.ImageField(
        upload_to='comptes_bancaires/', 
        blank=True, 
        null=True, 
        verbose_name=_("Image du compte"),
        help_text=_("Image ou document associé au compte bancaire")
    )
    actif = models.BooleanField(
        default=True, 
        verbose_name=_("Compte actif"),
        help_text=_("Indique si le compte bancaire est actuellement actif")
    )
    
    class Meta:
        verbose_name = _("Compte Bancaire")
        verbose_name_plural = _("Comptes Bancaires")
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.code})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.image.width = 400
            self.image.height = 300

class ModePaiement(models.Model):
    code = models.CharField(
        verbose_name=_("Code du mode de paiement"),
        max_length=50,
    )
    nom = models.CharField(
        verbose_name=_("Nom du mode de paiement"),
        max_length=100
    )
    actif = models.BooleanField(
        verbose_name=_("Actif"),
        default=True
    )

    class Meta:
        verbose_name = _("Mode de Paiement")
        verbose_name_plural = _("Modes de Paiement")
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En Attente'),
        ('confirme', 'Confirmé'),
        ('rejete', 'Rejeté'),
        ('rembourse', 'Remboursé'),
    ]

    souscripteur_physique = models.ForeignKey(
        SouscripteurPhysique, 
        on_delete=models.CASCADE, 
        verbose_name=_("Souscripteur Physique"),
        null=True,
        blank=True,
        related_name='paiements'
    )
    souscripteur_morale = models.ForeignKey(
        SouscripteurMorale, 
        on_delete=models.CASCADE, 
        verbose_name=_("Souscripteur Morale"),
        null=True,
        blank=True,
        related_name='paiements'
    )
    date_paiement = models.DateTimeField(
        verbose_name=_("Date et Heure du Paiement"),
        auto_now_add=True,
        help_text=_("Date et heure exactes de l'enregistrement du paiement")
    )

    mode_paiement = models.ForeignKey(
        ModePaiement,
        on_delete=models.PROTECT,
        verbose_name=_("Mode de Paiement")
    )
    numero_transaction = models.CharField(
        verbose_name=_("Numéro de Transaction"),
        max_length=100,
    )
    montant_souscription = models.DecimalField(
        verbose_name=_("Montant"),
        max_digits=15,
        decimal_places=2
    )
    statut = models.CharField(
        verbose_name=_("Statut du Paiement"),
        max_length=50,
        choices=STATUT_CHOICES,
        default='en_attente'
    )



    class Meta:
        verbose_name = _("Paiement")
        verbose_name_plural = _("Paiements")
        ordering = ['-date_paiement']
        constraints = [
            models.CheckConstraint(
                check=models.Q(souscripteur_physique__isnull=False) | 
                      models.Q(souscripteur_morale__isnull=False),
                name='souscripteur_not_null'
            )
        ]

    def __str__(self):
        souscripteur = self.souscripteur_physique or self.souscripteur_morale
        return f"Paiement de {souscripteur} - {self.numero_transaction}"
