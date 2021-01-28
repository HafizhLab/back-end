# Generated by Django 3.1.5 on 2021-01-27 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quran', '0002_load_quran_data'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=False)),
                ('mode', models.CharField(choices=[('ayah', 'Ayah Based'), ('word', 'Word Based')], max_length=4)),
                ('scope_id', models.PositiveSmallIntegerField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('scope_ct', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'quran'), ('model', 'Juz')), models.Q(('app_label', 'quran'), ('model', 'Surah')), _connector='OR'), on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options', models.JSONField()),
                ('ayah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.ayah')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
            ],
        ),
    ]
