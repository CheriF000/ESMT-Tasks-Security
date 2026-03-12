from django.db import models
from django.contrib.auth.models import User

# Profil utilisateur (étudiant ou professeur)
class Profil(models.Model):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Projet
class Projet(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_crees')
    membres = models.ManyToManyField(User, related_name='projets_membres', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre



class Tache(models.Model):
    STATUT_CHOICES = [
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_limite = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_faire')
    assigne_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taches_assignees')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def est_termine_dans_delai(self):
        """Vérifie si la tâche est terminée dans les délais (pour le calcul des primes)"""
        from django.utils import timezone
        if self.statut == 'termine':
            return timezone.now().date() <= self.date_limite
        return False