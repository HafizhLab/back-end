from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from hafizhlab.challenges.models import Challenge
from hafizhlab.games.models import GameSession
from hafizhlab.games.serializers import GameSessionSerializer
from hafizhlab.quran.models import Juz, Surah


class GameSessionSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.challenge = Challenge.objects.create(
            mode=Challenge.Mode.AYAH_BASED,
            scope=Juz(id=1),
        )

    def test_deserialize_pick_challenge(self):
        serializer = GameSessionSerializer(data={
            'challenge_id': self.challenge.id,
        })
        self.assertTrue(serializer.is_valid())

        game = serializer.save()
        self.assertEqual(game.challenge_id, self.challenge.id)
        self.assertEqual(game.mode, GameSession.Mode.SINGLE_PLAYER)

    def test_deserialize_single_player(self):
        serializer = GameSessionSerializer(data={
            'mode': GameSession.Mode.SINGLE_PLAYER,
            'config': {
                'mode': Challenge.Mode.WORD_BASED,
                'scope_ct': ContentType.objects.get_for_model(Juz).id,
                'scope_id': 3,
            },
        })
        self.assertTrue(serializer.is_valid())

        game = serializer.save()
        self.assertEqual(game.mode, GameSession.Mode.SINGLE_PLAYER)
        self.assertEqual(game.challenge.mode, Challenge.Mode.WORD_BASED)
        self.assertEqual(game.challenge.scope, Juz(id=3))

    def test_deserialize_multi_player(self):
        serializer = GameSessionSerializer(data={
            'mode': GameSession.Mode.MULTI_PLAYER,
            'config': {
                'mode': Challenge.Mode.WORD_BASED,
                'scope_ct': ContentType.objects.get_for_model(Surah).id,
                'scope_id': 4,
            },
        })
        self.assertTrue(serializer.is_valid())

        game = serializer.save()
        self.assertEqual(game.mode, GameSession.Mode.MULTI_PLAYER)
        self.assertEqual(game.challenge.mode, Challenge.Mode.WORD_BASED)
        self.assertEqual(game.challenge.scope, Surah(id=4))
