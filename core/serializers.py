from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profil, Projet, Tache


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profil
        fields = ['id', 'user', 'role', 'avatar', 'bio']


class TacheSerializer(serializers.ModelSerializer):
    assigne_a = UserSerializer(read_only=True)
    assigne_a_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigne_a', write_only=True, required=False
    )

    class Meta:
        model = Tache
        fields = ['id', 'titre', 'description', 'date_limite', 'statut', 'assigne_a', 'assigne_a_id', 'projet']


class ProjetSerializer(serializers.ModelSerializer):
    createur = UserSerializer(read_only=True)
    taches = TacheSerializer(many=True, read_only=True)
    membres = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Projet
        fields = ['id', 'titre', 'description', 'createur', 'membres', 'taches', 'date_creation']