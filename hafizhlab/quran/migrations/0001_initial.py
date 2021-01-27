# Generated by Django 3.1.5 on 2021-01-27 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Juz',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'juz',
                'verbose_name_plural': 'juzs',
            },
        ),
        migrations.CreateModel(
            name='Surah',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('english_name', models.CharField(max_length=14)),
            ],
            options={
                'verbose_name': 'surah',
                'verbose_name_plural': 'surahs',
            },
        ),
        migrations.CreateModel(
            name='Ayah',
            fields=[
                ('id', models.CharField(editable=False, max_length=6, primary_key=True, serialize=False)),
                ('number', models.PositiveSmallIntegerField()),
                ('text', models.TextField()),
                ('juz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.juz')),
                ('surah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.surah')),
            ],
            options={
                'verbose_name': 'ayah',
                'verbose_name_plural': 'ayahs',
            },
        ),
        migrations.AddConstraint(
            model_name='ayah',
            constraint=models.UniqueConstraint(fields=('surah', 'number'), name='unique_number_in_surah'),
        ),
    ]
