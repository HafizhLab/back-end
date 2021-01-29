from django.contrib import admin

from hafizhlab.quran.models import Ayah, Juz, Surah

admin.site.register(Ayah)
admin.site.register(Juz)
admin.site.register(Surah)
