# Generated by Django 4.2.7 on 2023-11-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0010_genre_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='anime_type',
            field=models.CharField(default='ТВ-Сериал', max_length=255),
        ),
    ]
