from django.contrib.auth.models import User
from django.utils import timezone

from .models import Note
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import Http404


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
        categories_list = notes.values_list('category', flat=True).distinct()
        return render(request, 'Note/index.html', context={
            'user': request.user, 'notes': notes, 'categories': categories_list
        })
    else:
        return redirect('Note:login_page')


def category(request, category):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user, category=category)
        if notes:
            return render(request, 'Note/category.html', context={'notes': notes, 'category': category})
        else:
            raise Http404('Page not found')
    else:
        return redirect('Note:login_page')


def details(request, note_id):
    if request.user.is_authenticated:
        note = Note.objects.filter(pk=note_id, user=request.user)
        if note:
            return render(request, 'Note/details.html', context={'note': note[0]})
        else:
            raise Http404('Page not found')
    else:
        return redirect('Note:login_page')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'Note/logout.html')
    else:
        raise Http404('Page not found')


def login_view(request):
    return render(request, 'Note/login.html')


def login_validate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('Note:index')
    else:
        return render(request, 'Note/login.html', context={'message': 'Bad username or password'})


def post_note(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        title = request.POST['title']
        text = request.POST['text']
        category = request.POST['category']
        mod_date = timezone.now()

        note = Note.objects.create(user=user, title=title, text=text, category=category, modification_date=mod_date)

        return redirect('Note:details', note_id=note.id)
    else:
        return redirect('Note:login_page')


def post_page(request):
    return render(request, 'Note/new_note.html')
