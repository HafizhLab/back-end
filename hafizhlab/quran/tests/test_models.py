from django.test import TestCase

from hafizhlab.quran.models import Chapter, Juz, Verse


class VerseTestCase(TestCase):

    def test_generated_verse_id(self):
        """Test verse id is generated properly based on verse chapter
        and verse number.
        """

        j = Juz.objects.create(id=1)
        c = Chapter.objects.create(id=2)

        v = Verse(juz=j, chapter=c, number=128)
        v.save()

        self.assertEqual(v.id, '2:128')
