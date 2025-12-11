from django.db import models

# Create your models here.
import uuid
from django.utils import timezone

class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_fichier = models.CharField(max_length=255)
    fichier_csv = models.FileField(upload_to='datasets/')
    data_upload = models.DateTimeField(default=timezone.now)
    stats_csv = models.FileField(upload_to='stats/', null=True, blank=True)
    notes_numpy = models.FileField(upload_to='notes_numpy/', null=True, blank=True)