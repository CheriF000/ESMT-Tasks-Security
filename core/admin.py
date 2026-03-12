from django.contrib import admin
from .models import Profil, Projet, Tache

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'createur', 'date_creation']
    filter_horizontal = ['membres']

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ['titre', 'projet', 'statut', 'assigne_a', 'date_limite']
    list_filter = ['statut']