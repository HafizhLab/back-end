from django.db import models

from hafizhlab.quran.models import Ayah


class Progress(models.Model):
    id = models.PositiveSmallIntegerField()
    ayah = models.ForeignKey(Ayah, on_delete=models.CASCADE)
    memorized = models.BooleanField()
    tested = models.BooleanField()
