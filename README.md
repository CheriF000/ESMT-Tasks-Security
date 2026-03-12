# ESMT - Application de Gestion des Tâches Collaboratives

Application web développée avec Django pour gérer des tâches dans un environnement collaboratif pour les enseignants et étudiants de l'ESMT.



##  Fonctionnalités

- **Gestion des utilisateurs** : Inscription, connexion, profils (Étudiant / Professeur)
- **Gestion des projets** : Créer, modifier, supprimer des projets et gérer les membres
- **Gestion des tâches** : Créer, assigner, modifier le statut des tâches avec filtres et recherche
- **Permissions et rôles** : Les étudiants ne peuvent pas assigner des professeurs
- **Statistiques** : Suivi trimestriel et annuel des tâches avec calcul des primes
- **API REST** : Endpoints RESTful avec authentification JWT
- **Tests** : 13 tests unitaires avec pytest-django

---

##  Système de primes

| Taux de complétion dans les délais | Prime |
|---|---|
| 100% | 100 000 FCFA |
| 90% ou plus | 30 000 FCFA |
| Moins de 90% | Pas de prime |

---

## Installation

### Prérequis
- Python 3.10+
- pip

### Étapes

**1. Cloner le projet**
```bash
git clone https://github.com/votre-username/gestion_taches.git
cd gestion_taches
```

**2. Créer et activer l'environnement virtuel**
```bash

python -m venv .venv
.venv\Scripts\activate



**3. Installer les dépendances**
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-allauth pillow pytest-django
```

**4. Appliquer les migrations**
```bash
python manage.py migrate
```

**5. Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

**6. Lancer le serveur**
```bash
python manage.py runserver
```

L'application est accessible sur **http://127.0.0.1:8000**

---

## Structure du projet

```
gestion_taches/
├── config/
│   ├── settings.py       # Configuration Django
│   ├── urls.py           # URLs principales
├── core/
│   ├── models.py         # Modèles : Profil, Projet, Tache
│   ├── views.py          # Vues Django (Templates)
│   ├── api_views.py      # Vues API REST
│   ├── serializers.py    # Sérialiseurs DRF
│   ├── forms.py          # Formulaires
│   ├── urls.py           # URLs de l'app
│   ├── api_urls.py       # URLs de l'API
│   ├── admin.py          # Interface d'administration
│   ├── tests.py          # Tests unitaires
│   └── templates/core/   # Templates HTML
├── manage.py
└── README.md
```

---

## Modèles de données

### Profil
| Champ | Type | Description |
|---|---|---|
| user | OneToOne(User) | Utilisateur Django |
| role | CharField | etudiant ou professeur |
| avatar | ImageField | Photo de profil |
| bio | TextField | Biographie |

### Projet
| Champ | Type | Description |
|---|---|---|
| titre | CharField | Titre du projet |
| description | TextField | Description |
| createur | ForeignKey(User) | Créateur du projet |
| membres | ManyToMany(User) | Membres du projet |
| date_creation | DateTimeField | Date de création |

### Tache
| Champ | Type | Description |
|---|---|---|
| projet | ForeignKey(Projet) | Projet associé |
| titre | CharField | Titre de la tâche |
| description | TextField | Description |
| date_limite | DateField | Date limite |
| statut | CharField | a_faire / en_cours / termine |
| assigne_a | ForeignKey(User) | Utilisateur assigné |

---

## Routes API

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtenir un token JWT |
| POST | `/api/token/refresh/` | Rafraîchir le token |
| GET/POST | `/api/projets/` | Liste / Créer projets |
| GET/PUT/DELETE | `/api/projets/{id}/` | Détail / Modifier / Supprimer projet |
| GET/POST | `/api/taches/` | Liste / Créer tâches |
| GET/PUT/DELETE | `/api/taches/{id}/` | Détail / Modifier / Supprimer tâche |
| GET | `/api/users/` | Liste des utilisateurs |
| GET | `/api/users/me/` | Utilisateur connecté |
| GET | `/api/profils/` | Profil de l'utilisateur connecté |

### Exemple d'utilisation de l'API avec JWT

```bash
# 1. Obtenir un token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "motdepasse"}'

# 2. Utiliser le token
curl http://127.0.0.1:8000/api/projets/ \
  -H "Authorization: Bearer <votre_token>"
```

---

## Lancer les tests

```bash
pytest
```

13 tests couvrant :
- Création des modèles
- Vues (inscription, connexion, dashboard, projets)
- Permissions (accès refusé pour non-créateur)
- Calcul des primes

---

## Technologies utilisées

| Technologie | Usage |
|---|---|
| Django 6.0 | Framework backend |
| Django REST Framework | API RESTful |
| djangorestframework-simplejwt | Authentification JWT |
| django-allauth | Gestion avancée des comptes |
| django-cors-headers | Support CORS pour frontend |
| SQLite | Base de données |
| Bootstrap 5 | Interface utilisateur |
| pytest-django | Tests unitaires |

---

MOUHAMADOU CHERIF KANE

