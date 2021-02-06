from django.urls import path
from . import views

app_name = 'Note'
urlpatterns = [
    path("", views.index, name='index'),
    path("category/<category>", views.category, name='category'),
    path("details/<note_id>", views.details, name='details'),
    path("logout", views.logout_view, name='logout'),
    path("login_validate", views.login_validate, name='login_validate'),
    path("login", views.login_view, name='login_page'),
    path("post_note", views.post_note, name='post_note'),
    path("new_note", views.post_page, name='new_note'),
    path("serach_note", views.search_note, name='search_note'),
    path("edit_page/<note_id>", views.edit_page, name='edit_page'),
    path("edit_note", views.edit_note, name='edit_note'),
    path("register", views.register_view, name='register_page'),
    path("register_account", views.register_account, name='register_account')
]
