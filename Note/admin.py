from django.contrib import admin
from .models import Note, File


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'modification_date', 'user')


admin.site.register(Note, NoteAdmin)
admin.site.register(File)
