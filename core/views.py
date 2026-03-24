from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from .forms import InscriptionForm, ProfilForm, ProjetForm, TacheForm
from .models import Profil, Projet, Tache

ACCES_REFUSE = 'Accès refusé.'


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('dashboard')
    else:
        form = InscriptionForm()
    return render(request, 'core/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects.')
    return render(request, 'core/connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('connexion')


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required
def modifier_profil(request):
    profil = request.user.profil
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour !')
            return redirect('mon_profil')
    else:
        form = ProfilForm(instance=profil, user=request.user)
    return render(request, 'core/modifier_profil.html', {'form': form})


@login_required
def mon_profil(request):
    profil = request.user.profil
    return render(request, 'core/mon_profil.html', {'profil': profil})


@login_required
def liste_projets(request):
    projets_crees = Projet.objects.filter(createur=request.user)
    projets_membres = Projet.objects.filter(membres=request.user)
    return render(request, 'core/liste_projets.html', {
        'projets_crees': projets_crees,
        'projets_membres': projets_membres,
    })


@login_required
def creer_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.createur = request.user
            projet.save()
            form.save_m2m()
            messages.success(request, 'Projet créé avec succès !')
            return redirect('liste_projets')
    else:
        form = ProjetForm()
    return render(request, 'core/projet_form.html', {'form': form, 'titre': 'Créer un projet'})


@login_required
def modifier_projet(request, pk):
    projet = get_object_or_404(Projet, pk=pk, createur=request.user)
    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projet modifié avec succès !')
            return redirect('liste_projets')
    else:
        form = ProjetForm(instance=projet)
    return render(request, 'core/projet_form.html', {'form': form, 'titre': 'Modifier le projet'})


@login_required
def supprimer_projet(request, pk):
    projet = get_object_or_404(Projet, pk=pk, createur=request.user)
    if request.method == 'POST':
        projet.delete()
        messages.success(request, 'Projet supprimé !')
        return redirect('liste_projets')
    return render(request, 'core/confirmer_suppression.html', {'objet': projet})


@login_required
def detail_projet(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.user != projet.createur and request.user not in projet.membres.all():
        messages.error(request, ACCES_REFUSE)
        return redirect('liste_projets')
    taches = projet.taches.all()
    return render(request, 'core/detail_projet.html', {'projet': projet, 'taches': taches})


@login_required
def creer_tache(request, pk):
    projet = get_object_or_404(Projet, pk=pk, createur=request.user)
    if request.method == 'POST':
        form = TacheForm(request.POST, projet=projet, user=request.user)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.projet = projet
            tache.save()
            messages.success(request, 'Tâche créée avec succès !')
            return redirect('detail_projet', pk=projet.pk)
    else:
        form = TacheForm(projet=projet, user=request.user)
    return render(request, 'core/tache_form.html', {'form': form, 'projet': projet, 'titre': 'Créer une tâche'})


@login_required
def modifier_tache(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    projet = tache.projet
    if request.user != projet.createur and request.user != tache.assigne_a:
        messages.error(request, ACCES_REFUSE)
        return redirect('detail_projet', pk=projet.pk)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache, projet=projet, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tâche modifiée avec succès !')
            return redirect('detail_projet', pk=projet.pk)
    else:
        form = TacheForm(instance=tache, projet=projet, user=request.user)
    return render(request, 'core/tache_form.html', {'form': form, 'projet': projet, 'titre': 'Modifier la tâche'})


@login_required
def supprimer_tache(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    projet = tache.projet
    if request.user != projet.createur:
        messages.error(request, ACCES_REFUSE)
        return redirect('detail_projet', pk=projet.pk)
    if request.method == 'POST':
        tache.delete()
        messages.success(request, 'Tâche supprimée !')
        return redirect('detail_projet', pk=projet.pk)
    return render(request, 'core/confirmer_suppression.html', {'objet': tache})


@login_required
def mes_taches(request):
    taches = Tache.objects.filter(assigne_a=request.user)
    statut = request.GET.get('statut')
    projet_id = request.GET.get('projet')
    recherche = request.GET.get('q')
    if statut:
        taches = taches.filter(statut=statut)
    if projet_id:
        taches = taches.filter(projet__id=projet_id)
    if recherche:
        taches = taches.filter(titre__icontains=recherche)
    projets = Projet.objects.filter(membres=request.user) | Projet.objects.filter(createur=request.user)
    return render(request, 'core/mes_taches.html', {
        'taches': taches,
        'projets': projets,
        'statut_actif': statut,
        'projet_actif': projet_id,
        'recherche': recherche,
    })


@login_required
def statistiques(request):
    today = timezone.now().date()
    trimestre = today.month // 4 + 1
    annee = today.year
    debut_trimestre = today.replace(month=((today.month - 1) // 3) * 3 + 1, day=1)
    utilisateurs = User.objects.filter(profil__role='professeur')
    stats = []
    for u in utilisateurs:
        taches_annee = Tache.objects.filter(assigne_a=u, date_limite__year=annee)
        total_annee = taches_annee.count()
        terminees_annee = taches_annee.filter(statut='termine').count()
        dans_delai_annee = sum(1 for t in taches_annee.filter(statut='termine') if t.est_termine_dans_delai())
        taches_trim = taches_annee.filter(date_limite__gte=debut_trimestre)
        total_trim = taches_trim.count()
        terminees_trim = taches_trim.filter(statut='termine').count()
        prime = 0
        if total_annee > 0:
            taux = dans_delai_annee / total_annee * 100
            if taux == 100:
                prime = 100000
            elif taux >= 90:
                prime = 30000
        stats.append({
            'user': u,
            'total_annee': total_annee,
            'terminees_annee': terminees_annee,
            'dans_delai_annee': dans_delai_annee,
            'taux_annee': round(dans_delai_annee / total_annee * 100, 1) if total_annee > 0 else 0,
            'total_trim': total_trim,
            'terminees_trim': terminees_trim,
            'prime': prime,
        })
    return render(request, 'core/statistiques.html', {
        'stats': stats,
        'annee': annee,
        'trimestre': trimestre,
    })