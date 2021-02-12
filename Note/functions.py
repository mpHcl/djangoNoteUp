import re

from django.core.files.storage import FileSystemStorage
from .models import File
from NoteUp.settings import MEDIA_ROOT


# Applies to file upload. It saves file in Media folder and saving path in database
def handle_file(file, note):
    fs = FileSystemStorage(location=MEDIA_ROOT + "\\note_files\\")
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)

    File.objects.create(note=note, file="note_files" + file_url).save()


# Applies to register page, this is checking if given email is valid
def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if (re.search(regex, email)):
        return True
    else:
        return False
