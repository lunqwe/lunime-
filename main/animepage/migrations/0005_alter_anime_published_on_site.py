# Generated by Django 4.2.7 on 2023-11-18 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0004_anime_published_on_site_anime_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='published_on_site',
            field=models.DateField(auto_created=True, default='2023-11-19'),
        ),
    ]
