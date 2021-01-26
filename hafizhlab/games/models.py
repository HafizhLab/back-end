import uuid

from django.conf import settings
from django.db import models

from hafizhlab.challenges.models import Challenge


def generate_challenge():
    return Challenge.objects.create()


class GameSession(models.Model):
    class Mode(models.IntegerChoices):
        SINGLE_PLAYER = 1
        MULTI_PLAYER = 2

    room_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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
    mode = models.PositiveSmallIntegerField(choices=Mode.choices)
