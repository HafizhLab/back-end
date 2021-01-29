import random
import uuid

from django.conf import settings
from django.db import models

from hafizhlab.challenges.models import Challenge


def generate_public_code():
    retry = True
    while retry:
        public_code = str(random.randrange(10000)).zfill(4)
        retry = GameSession.objects.filter(public_code=public_code).exists()
    return public_code


def generate_challenge():
    return Challenge.objects.create()


class GameSession(models.Model):
    class Mode(models.TextChoices):
        SINGLE_PLAYER = 'single'
        MULTI_PLAYER = 'multi'

    room_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    public_code = models.CharField(
        max_length=4,
        default=generate_public_code,
        editable=False,
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    challenge = models.ForeignKey(
        'challenges.Challenge',
        on_delete=models.PROTECT,
        default=generate_challenge,
    )
    mode = models.CharField(
        max_length=6,
        choices=Mode.choices,
        default=Mode.SINGLE_PLAYER,
    )
