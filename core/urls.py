from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='connexion'),
    path('logout/', views.deconnexion, name='deconnexion'),
    path('profil/', views.mon_profil, name='mon_profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('taches/', views.mes_taches, name='mes_taches'),

    # Projets
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projets/creer/', views.creer_projet, name='creer_projet'),
    path('projets/<int:pk>/', views.detail_projet, name='detail_projet'),
    path('projets/<int:pk>/modifier/', views.modifier_projet, name='modifier_projet'),
    path('projets/<int:pk>/supprimer/', views.supprimer_projet, name='supprimer_projet'),

    # Tâches
    path('projets/<int:pk>/taches/creer/', views.creer_tache, name='creer_tache'),
    path('taches/<int:pk>/modifier/', views.modifier_tache, name='modifier_tache'),
    path('taches/<int:pk>/supprimer/', views.supprimer_tache, name='supprimer_tache'),

    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),
]