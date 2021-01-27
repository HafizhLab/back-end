from django.test import TestCase

from hafizhlab.quran.models import Ayah, Juz, Surah


class Migration0002TestCase(TestCase):

    def test_count_data_loaded(self):
        """Test number of data loaded from data migration"""
        self.assertEqual(Juz.objects.count(), 30)
        self.assertEqual(Surah.objects.count(), 114)
        self.assertEqual(Ayah.objects.count(), 6236)
