# Generated by Django 4.2.7 on 2023-12-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0034_remove_additionalname_anime_remove_episode_anime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='description',
            field=models.CharField(default=0, max_length=900),
        ),
    ]
