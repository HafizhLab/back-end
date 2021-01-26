from django.conf import settings
from django.db import models


class Challenge(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )


class Question(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    text = models.ForeignKey('quran.Ayah', on_delete=models.CASCADE)
    options = models.CharField(max_length=1000)
