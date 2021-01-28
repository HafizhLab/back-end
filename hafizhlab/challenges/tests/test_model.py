from django.core.exceptions import ValidationError
from django.test import TestCase

from hafizhlab.challenges.models import Challenge, Question
from hafizhlab.quran.models import Ayah, Juz, Surah


class QuestionTest(TestCase):
    def test_question_ayah_out_of_scope(self):
        scope_juz_id = 1
        out_ayah_id = Ayah.objects.filter(juz_id=2).values_list('id', flat=True).first()
        in_ayah_ids = Ayah.objects.filter(juz_id=1).values_list('id', flat=True)[:3]

        challenge = Challenge.objects.create(
            mode=Challenge.Mode.AYAH_BASED,
            scope=Juz(id=scope_juz_id),
        )

        with self.assertRaises(ValidationError):
            question = Question(
                challenge=challenge,
                ayah_id=out_ayah_id,
                options=[
                    out_ayah_id,
                    *in_ayah_ids,
                ]
            )
            question.full_clean()

    def test_question_answer_not_exist(self):
        with self.assertRaises(ValidationError):
            challenge1 = Challenge.objects.create(
                mode=Challenge.Mode.AYAH_BASED,
                scope=Juz(id=1),
            )

            question1 = Question(
                challenge=challenge1,
                ayah_id=1,
                options=[2, 3, 4, 5],
            )
            question1.full_clean()

        with self.assertRaises(ValidationError):
            challenge2 = Challenge.objects.create(
                mode=Challenge.Mode.WORD_BASED,
                scope=Surah(id=2),
            )

            question2 = Question(
                challenge=challenge2,
                ayah=Ayah.objects.get(surah_id=2, number=1),
                options=['a', 'b', 'c', 'd'],
            )
            question2.full_clean()

    def test_question_options_correct_format(self):
        question1 = Question(
            challenge=Challenge.objects.create(
                mode=Challenge.Mode.AYAH_BASED,
                scope=Juz(id=1),
            ),
            ayah_id=1,
            options=[1, 2, 3, 4],
        )
        question1.full_clean()

        question2 = Question(
            challenge=Challenge.objects.create(
                mode=Challenge.Mode.WORD_BASED,
                scope=Surah(id=1),
            ),
            ayah=Ayah.objects.get(surah_id=1, number=2),
            options=[
                [ans, *other.split()[:3]]
                for ans, other in zip(
                    Ayah.objects.get(surah_id=1, number=2).text.split(),
                    Ayah.objects.filter(surah_id=1, number__in=[4, 5, 6, 7]).values_list('text', flat=True),
                )
            ],
        )
        question2.full_clean()
