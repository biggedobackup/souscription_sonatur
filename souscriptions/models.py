from django.db import models
from django.utils.translation import gettext_lazy as _

class TypeSouscripteur(models.Model):
    # Constantes pour les types de souscripteurs
    PERSONNE_PHYSIQUE = 'Personne Physique'
    PERSONNE_MORALE = 'Personne Morale'
    
    TYPE_CHOICES = [
        (PERSONNE_PHYSIQUE, 'Personne Physique'),
        (PERSONNE_MORALE, 'Personne Morale'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=100, choices=TYPE_CHOICES, verbose_name="Nom")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(
        verbose_name=_("Date et Heure de Création"),
        auto_now_add=True,
        help_text=_("Date et heure exactes de la création du type de souscripteur")
    )
    
    class Meta:
        verbose_name = "Type de Souscripteur"
        verbose_name_plural = "Types de Souscripteurs"
        
    def __str__(self):
        return self.nom

    @classmethod
    def get_type_physique(cls):
        return cls.objects.get_or_create(
            code='PHYSIQUE',
            defaults={
                'nom': cls.PERSONNE_PHYSIQUE,
                'description': 'Type pour les personnes physiques',
                'actif': True
            }
        )[0]

    @classmethod
    def get_type_moral(cls):
        return cls.objects.get_or_create(
            code='MORALE',
            defaults={
                'nom': cls.PERSONNE_MORALE,
                'description': 'Type pour les personnes morales',
                'actif': True
            }
        )[0]

class SouscripteurPhysique(models.Model):
    PAYS_CHOICES = [
        ('Burkina Faso', 'Burkina Faso'),
        ("Côte d'Ivoire", "Côte d'Ivoire"),
        ('Sénégal', 'Sénégal'),
        ('Mali', 'Mali'),
        ('Niger', 'Niger'),
        ('Togo', 'Togo'),
        ('Bénin', 'Bénin'),
        ('Guinée', 'Guinée'),
        ('Ghana', 'Ghana'),
        ('Nigéria', 'Nigéria'),
        ('Algérie', 'Algérie'),
        ('Afrique du Sud', 'Afrique du Sud'),
        ('Congo (RDC)', 'Congo (RDC)'),
        ('Kenya', 'Kenya'),
        ('Maroc', 'Maroc'),
        ('Tunisie', 'Tunisie'),
        ('Égypte', 'Égypte'),
        ('Tanzanie', 'Tanzanie'),
        ('Zambie', 'Zambie'),
        ('Ouganda', 'Ouganda'),
    ]

    DOCUMENT_CHOICES = [
        ('CIN', "Carte Nationale d'Identité Burkinabé"),
        ('PASSEPORT', 'Passeport'),
        ('PERMIS_SEJOUR', 'Permis de Séjour'),
        ('CARTE_RESIDENT', 'Carte de Résident'),
    ]

    GENRE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]

    type_souscripteur = models.ForeignKey(TypeSouscripteur, on_delete=models.SET_NULL, null=True, verbose_name="Type de Souscripteur")
    nom_complet = models.CharField(max_length=150, verbose_name="Nom Complet")
    email = models.EmailField( verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_naissance = models.DateField(verbose_name="Date de Naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de Naissance")
    profession = models.CharField(max_length=100, verbose_name="Profession")
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, verbose_name="Genre")
    document = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, verbose_name="Type de Document")
    numero_piece = models.CharField(max_length=50, verbose_name="Numéro de Pièce")
    date_expiration = models.DateField(verbose_name="Date d'Expiration")
    lieu_etablissement = models.CharField(max_length=100, verbose_name="Lieu d'Établissement")
    date_etablissement = models.DateField(verbose_name="Date d'Établissement")
    pays = models.CharField(max_length=100, choices=PAYS_CHOICES, verbose_name="Pays")
    region = models.CharField(max_length=100, verbose_name="Région")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(
        verbose_name=_("Date et Heure de Création"),
        auto_now_add=True,
        help_text=_("Date et heure exactes de la création du souscripteur")
    )

    class Meta:
        verbose_name = "Souscripteur Physique"
        verbose_name_plural = "Souscripteurs Physiques"

    def __str__(self):
        return self.nom_complet

    def save(self, *args, **kwargs):
        # Assigner automatiquement le type physique
        if not self.type_souscripteur_id:
            self.type_souscripteur = TypeSouscripteur.get_type_physique()
        super().save(*args, **kwargs)

class SouscripteurMorale(models.Model):
    FORME_JURIDIQUE_CHOICES = [
        ('SA', 'SA'),
        ('SARL', 'SARL'),
        ('SAS', 'SAS'),
        ('AUTRE', 'Autre'),
    ]

    type_souscripteur = models.ForeignKey(TypeSouscripteur, on_delete=models.SET_NULL, null=True, verbose_name="Type de Souscripteur")
    raison_sociale = models.CharField(max_length=200, verbose_name="Raison Sociale")
    forme_juridique = models.CharField(max_length=20, choices=FORME_JURIDIQUE_CHOICES, verbose_name="Forme Juridique")
    rccm = models.CharField(max_length=50, null=True, blank=True, verbose_name="RCCM")
    ifu = models.CharField(max_length=50, null=True, blank=True, verbose_name="IFU")
    siege_social = models.CharField(max_length=200, verbose_name="Siège Social")
    nom_representant = models.CharField(max_length=100, verbose_name="Nom du Représentant")
    prenom_representant = models.CharField(max_length=100, verbose_name="Prénom du Représentant")
    fonction_representant = models.CharField(max_length=100, verbose_name="Fonction du Représentant")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    pays = models.CharField(max_length=100, choices=SouscripteurPhysique.PAYS_CHOICES, verbose_name="Pays")
    region = models.CharField(max_length=100, verbose_name="Région")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(
        verbose_name=_("Date et Heure de Création"),
        auto_now_add=True,
        help_text=_("Date et heure exactes de la création du souscripteur")
    )

    class Meta:
        verbose_name = "Souscripteur Moral"
        verbose_name_plural = "Souscripteurs Moraux"

    def __str__(self):
        return self.raison_sociale

    def save(self, *args, **kwargs):
        # Assigner automatiquement le type moral
        if not self.type_souscripteur_id:
            self.type_souscripteur = TypeSouscripteur.get_type_moral()
        super().save(*args, **kwargs)

class SouscriptionEffectuee(models.Model):
    # Informations de l'opération
    operation = models.ForeignKey('operations.Operations', on_delete=models.PROTECT, verbose_name="Opération")
    numero_transaction = models.CharField(max_length=50, unique=True, verbose_name="Numéro de Transaction")
    date_souscription = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Date et Heure de Souscription"),
        help_text=_("Date et heure exactes de l'enregistrement de la souscription")
    )
    duree_depot_physique = models.PositiveIntegerField(verbose_name="Durée pour le dépôt physique (en jours)", null=True)
    processus_attributions = models.ManyToManyField('operations.ProcessusAttribution', verbose_name="Processus d'Attribution", related_name='souscriptions')
    comptes_bancaires = models.ManyToManyField('paiements.CompteBancaire', verbose_name="Comptes Bancaires", related_name='souscriptions')
    
    # Statut de la souscription
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name="Statut"
    )
    
    # Informations du souscripteur
    type_souscripteur = models.ForeignKey(TypeSouscripteur, on_delete=models.PROTECT, verbose_name="Type de Souscripteur")
    
    # Pour personne physique
    nom_complet = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nom Complet")
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de Naissance")
    lieu_naissance = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de Naissance")
    profession = models.CharField(max_length=100, null=True, blank=True, verbose_name="Profession")
    genre = models.CharField(max_length=10, null=True, blank=True, verbose_name="Genre")
    document = models.CharField(max_length=20, null=True, blank=True, verbose_name="Type de Document")
    numero_piece = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numéro de Pièce")
    date_expiration = models.DateField(null=True, blank=True, verbose_name="Date d'Expiration")
    lieu_etablissement = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu d'Établissement")
    date_etablissement = models.DateField(null=True, blank=True, verbose_name="Date d'Établissement")
    
    # Pour personne morale
    raison_sociale = models.CharField(max_length=200, null=True, blank=True, verbose_name="Raison Sociale")
    forme_juridique = models.CharField(max_length=20, null=True, blank=True, verbose_name="Forme Juridique")
    rccm = models.CharField(max_length=50, null=True, blank=True, verbose_name="RCCM")
    ifu = models.CharField(max_length=50, null=True, blank=True, verbose_name="IFU")
    siege_social = models.CharField(max_length=200, null=True, blank=True, verbose_name="Siège Social")
    nom_representant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom du Représentant")
    prenom_representant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prénom du Représentant")
    fonction_representant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fonction du Représentant")
    
    # Informations communes
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    pays = models.CharField(max_length=100, verbose_name="Pays")
    region = models.CharField(max_length=100, verbose_name="Région")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    
    # Informations de la parcelle
    type_parcelle = models.ForeignKey('operations.TypeParcelle', on_delete=models.PROTECT, verbose_name="Type de Parcelle")
    parcelle = models.ForeignKey('operations.ListesParcelles', on_delete=models.PROTECT, verbose_name="Parcelle")
    position = models.ForeignKey('operations.PositionParcelle', on_delete=models.PROTECT, verbose_name="Position")
    surface = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Surface")
    cout_unitaire = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Coût Unitaire")
    prix_total = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Prix Total")
    acompte = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Acompte")
    reste_a_payer = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Reste à Payer")
    section = models.CharField(max_length=100, verbose_name="Section")
    lot = models.CharField(max_length=100, verbose_name="Lot")
    
    # Informations de paiement
    montant_souscription = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Frais de Souscription")
    methode_paiement = models.CharField(max_length=50, verbose_name="Méthode de Paiement")
    date_paiement = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Date et Heure de Paiement"),
        help_text=_("Date et heure exactes de l'enregistrement du paiement")
    )
    
    
    class Meta:
        verbose_name = "Souscription Effectuée"
        verbose_name_plural = "Souscriptions Effectuées"
        ordering = ['-date_souscription']
    
    def __str__(self):
        if self.type_souscripteur.code == 'PHYSIQUE':
            return f"Souscription de {self.nom_complet} - {self.numero_transaction}"
        return f"Souscription de {self.raison_sociale} - {self.numero_transaction}"
