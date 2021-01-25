from django.db import models
from django.utils.translation import gettext_lazy as _


class Juz(models.Model):
    """Simple representation of Quran's Juz"""
    id = models.PositiveSmallIntegerField(primary_key=True)

    class Meta:
        verbose_name = _('juz')
        verbose_name_plural = _('juzs')

    def __str__(self):
        return str(self.id)


class Surah(models.Model):
    """Simple representation of Quran's Surah"""
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    english_name = models.CharField(max_length=14)

    class Meta:
        verbose_name = _('surah')
        verbose_name_plural = _('surahs')

    def __str__(self):
        return str(self.name)


class Ayah(models.Model):
    """Simple representation of Quran's Ayah"""
    id = models.CharField(max_length=6, primary_key=True, editable=False)
    juz = models.ForeignKey(Juz, on_delete=models.CASCADE)
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        verbose_name = _('ayah')
        verbose_name_plural = _('ayahs')
        constraints = [
            models.UniqueConstraint(fields=['surah', 'number'],
                                    name='unique_number_in_surah'),
        ]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.id = '{}:{}'.format(self.surah.id, self.number)
        super().save(*args, **kwargs)
