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
]
