from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    category = models.CharField(max_length=100)
    text = models.TextField(max_length=3000)
    modification_date = models.DateTimeField('date_modified')

    def __str__(self):
        return str(self.title) + ' (' + str(self.category) + ')'


class File(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to="note_files")

    def __str__(self):
        return str("file_" + str(self.id))
