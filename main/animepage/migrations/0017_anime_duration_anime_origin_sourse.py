# Generated by Django 4.2.7 on 2023-11-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0016_rename_date_publised_anime_date_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='duration',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='anime',
            name='origin_sourse',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
