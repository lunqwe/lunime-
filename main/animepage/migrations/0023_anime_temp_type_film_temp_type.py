# Generated by Django 4.2.7 on 2023-11-27 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0022_rename_published_on_site_anime_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='temp_type',
            field=models.CharField(default='Anime', max_length=255),
        ),
        migrations.AddField(
            model_name='film',
            name='temp_type',
            field=models.CharField(default='Film', max_length=255),
        ),
    ]
