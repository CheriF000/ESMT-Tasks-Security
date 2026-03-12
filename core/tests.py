import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profil, Projet, Tache
from datetime import date


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='test1234')
    Profil.objects.create(user=user, role='professeur')
    return user

@pytest.fixture
def etudiant(db):
    user = User.objects.create_user(username='etudiant1', password='test1234')
    Profil.objects.create(user=user, role='etudiant')
    return user

@pytest.fixture
def projet(db, user):
    return Projet.objects.create(titre='Projet Test', createur=user)

@pytest.fixture
def tache(db, projet, user):
    return Tache.objects.create(
        titre='Tâche Test',
        projet=projet,
        date_limite=date(2026, 12, 31),
        statut='a_faire',
        assigne_a=user
    )



class TestModeles:
    def test_creation_profil(self, user):
        assert user.profil.role == 'professeur'

    def test_creation_projet(self, projet, user):
        assert projet.titre == 'Projet Test'
        assert projet.createur == user

    def test_creation_tache(self, tache):
        assert tache.titre == 'Tâche Test'
        assert tache.statut == 'a_faire'

    def test_tache_termine_dans_delai(self, tache):
        tache.statut = 'termine'
        tache.date_limite = date(2099, 12, 31)
        tache.save()
        assert tache.est_termine_dans_delai() == True

    def test_tache_hors_delai(self, tache):
        tache.statut = 'termine'
        tache.date_limite = date(2020, 1, 1)
        tache.save()
        assert tache.est_termine_dans_delai() == False



class TestVues:
    def test_inscription(self, client, db):
        response = client.post(reverse('inscription'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'role': 'etudiant',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()

    def test_connexion(self, client, user):
        response = client.post(reverse('connexion'), {
            'username': 'testuser',
            'password': 'test1234',
        })
        assert response.status_code == 302

    def test_dashboard_non_connecte(self, client):
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302  # redirige vers login

    def test_dashboard_connecte(self, client, user):
        client.login(username='testuser', password='test1234')
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200

    def test_creer_projet(self, client, user):
        client.login(username='testuser', password='test1234')
        response = client.post(reverse('creer_projet'), {
            'titre': 'Nouveau Projet',
            'description': 'Description test',
        })
        assert response.status_code == 302
        assert Projet.objects.filter(titre='Nouveau Projet').exists()

    def test_supprimer_projet_non_createur(self, client, etudiant, projet):
        client.login(username='etudiant1', password='test1234')
        response = client.post(reverse('supprimer_projet', args=[projet.pk]))
        assert response.status_code == 404  # accès refusé



class TestPrimes:
    def test_prime_100k(self, tache, user):
        tache.statut = 'termine'
        tache.date_limite = date(2099, 12, 31)
        tache.save()
        taches = Tache.objects.filter(assigne_a=user)
        total = taches.count()
        dans_delai = sum(1 for t in taches if t.est_termine_dans_delai())
        taux = dans_delai / total * 100 if total > 0 else 0
        prime = 100000 if taux == 100 else (30000 if taux >= 90 else 0)
        assert prime == 100000

    def test_pas_de_prime(self, tache, user):
        tache.statut = 'a_faire'
        tache.save()
        taches = Tache.objects.filter(assigne_a=user)
        total = taches.count()
        dans_delai = sum(1 for t in taches if t.est_termine_dans_delai())
        taux = dans_delai / total * 100 if total > 0 else 0
        prime = 100000 if taux == 100 else (30000 if taux >= 90 else 0)
        assert prime == 0