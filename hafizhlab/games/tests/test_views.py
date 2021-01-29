import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from hafizhlab.challenges.models import Challenge
from hafizhlab.games.models import GameSession
from hafizhlab.quran.models import Juz, Surah

User = get_user_model()


class GameSessionAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create()
        cls.user_token = Token.objects.create(user=cls.user)
        cls.challenge = Challenge.objects.create(
            mode=Challenge.Mode.AYAH_BASED,
            scope=Juz(id=1),
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('game-list')

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.user_token.key))

    def test_play_a_challenge(self):
        response = self.client.post(
            self.url,
            {'challenge_id': self.challenge.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GameSession.objects.filter(
            room_id=json.loads(response.content)['room_id'],
            challenge_id=self.challenge.id,
            mode=GameSession.Mode.SINGLE_PLAYER,
        ).exists())

    def test_create_practice_game(self):
        response = self.client.post(
            self.url,
            {
                'mode': 'single',
                'config': {
                    'mode': Challenge.Mode.AYAH_BASED,
                    'scope_ct': ContentType.objects.get_for_model(Juz).id,
                    'scope_id': 1,
                }
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game_q = GameSession.objects.filter(
            room_id=json.loads(response.content)['room_id'],
            mode=GameSession.Mode.SINGLE_PLAYER,
        )
        self.assertTrue(game_q.exists())
        self.assertTrue(Challenge.objects.filter(
            id=game_q.get().id,
            mode=Challenge.Mode.AYAH_BASED,
            scope_ct=ContentType.objects.get_for_model(Juz).id,
            scope_id=1,
        ).exists())

    def test_create_multiplayer_game(self):
        response = self.client.post(
            self.url,
            {
                'mode': 'multi',
                'config': {
                    'mode': Challenge.Mode.WORD_BASED,
                    'scope_ct': ContentType.objects.get_for_model(Surah).id,
                    'scope_id': 2,
                },
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game_q = GameSession.objects.filter(
            room_id=json.loads(response.content)['room_id'],
            admin=self.user.id,
            mode=GameSession.Mode.MULTI_PLAYER,
        )
        self.assertTrue(game_q.exists())
        self.assertTrue(Challenge.objects.filter(
            id=game_q.get().challenge.id,
            mode=Challenge.Mode.WORD_BASED,
            scope_ct=ContentType.objects.get_for_model(Surah).id,
            scope_id=2,
        ).exists())
