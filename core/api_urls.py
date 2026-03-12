from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'projets', api_views.ProjetViewSet, basename='api-projets')
router.register(r'taches', api_views.TacheViewSet, basename='api-taches')
router.register(r'users', api_views.UserViewSet, basename='api-users')
router.register(r'profils', api_views.ProfilViewSet, basename='api-profils')

urlpatterns = [
    path('', include(router.urls)),
]