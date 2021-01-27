from django.test import TestCase

from hafizhlab.quran.models import Ayah, Juz, Surah


class AyahTestCase(TestCase):

    def test_generated_ayah_id(self):
        """Test ayah id is generated properly based on ayah's surah
        and ayah's number.
        """

        j = Juz.objects.create(id=1)
        s = Surah.objects.create(id=2)

        v = Ayah(juz=j, surah=s, number=128)
        v.save()

        self.assertEqual(v.id, '2:128')
