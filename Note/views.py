from django.contrib.auth.models import User
from django.utils import timezone

from .functions import handle_file
from .models import Note, File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.http import Http404, HttpResponse, FileResponse
from .functions import check

from NoteUp.settings import MEDIA_ROOT


def index(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user).order_by('-modification_date')
        categories_list = notes.values_list('category', flat=True).distinct().order_by()
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
            files = File.objects.filter(note=note[0])
            return render(request, 'Note/details.html', context={'note': note[0], 'files': files})
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


def register_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'Note/register.html')


def register_account(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    if email and username and password and first_name and last_name:
        if not check(email):
            return render(request, "Note/register.html", context={'email_message': "Invalid email :/"})
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        logout(request)
        login(request, user)
        return redirect('Note:index')
    else:
        return render(request, "Note/register.html", context={'message': "Missing some information :/"})


def post_note(request):
    if request.user.is_authenticated and request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        title = request.POST['title']
        text = request.POST['text']
        category = request.POST['category']
        mod_date = timezone.now()

        if title and text and category:
            note = Note.objects.create(user=user, title=title, text=text, category=category, modification_date=mod_date)

            if request.FILES:
                handle_file(file=request.FILES['myfile'], note=note)

            return redirect('Note:details', note_id=note.id)
        else:
            return redirect('Note:new_note')
    else:
        return redirect('Note:login_page')


def edit_note(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        note_id = request.POST['id']
        title = request.POST['title']
        text = request.POST['text']
        category = request.POST['category']
        mod_date = timezone.now()

        note = get_object_or_404(Note, user=user, pk=note_id)
        if title and text and category:
            note.title = title
            note.category = category
            note.modification_date = mod_date
            note.text = text
            note.save()

            if request.FILES:
                handle_file(file=request.FILES['myfile'], note=note)

            return redirect('Note:details', note_id=note.id)
        else:
            return redirect('Note:new_note')
    else:
        return redirect('Note:login_page')


def post_page(request):
    return render(request, 'Note/new_note.html')


def edit_page(request, note_id):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, pk=note_id, user=request.user)
        return render(request, 'Note/new_note.html', context={'note': note, 'edit': True})
    else:
        return redirect('Note:login_page')


def search_note(request):
    if request.user.is_authenticated:
        search_value = request.POST['value']
        notes = Note.objects.filter(user=request.user, title__contains=search_value).order_by('-modification_date')
        categories_list = notes.values_list('category', flat=True).distinct().order_by()
        return render(request, 'Note/index.html', context={
            'user': request.user, 'notes': notes, 'categories': categories_list
        })
    else:
        return redirect('Note:login_page')


def download_file(reqeust, path, file):
    if reqeust.user.is_authenticated:
        notes = Note.objects.filter(user=reqeust.user)
        for note in notes:
            if File.objects.filter(note=note, file=path+"/"+file):
                return FileResponse(open(MEDIA_ROOT + "\\" + path + "\\" + file, 'rb'))

    return redirect('Note:login_page')
