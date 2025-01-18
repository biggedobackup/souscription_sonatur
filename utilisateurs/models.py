from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)



class Role(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
    
    def __str__(self):
        return self.nom

class Utilisateur(AbstractUser):
    username = None  # Désactiver le champ username
    nom_complet = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(unique=True, verbose_name="Email", max_length=100)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name="Rôle")
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_complet']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def get_full_name(self):
        return self.nom_complet or f"{self.first_name} {self.last_name}".strip() 
    
    def get_role_display(self):
        return self.role.nom if self.role else "Aucun rôle"
    
    def get_status_display(self):
        return "Actif" if self.is_active else "Inactif"
    
    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError({'email': 'L\'email est obligatoire'})
        if not self.role:
            raise ValidationError({'role': 'Le rôle est obligatoire'})
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)