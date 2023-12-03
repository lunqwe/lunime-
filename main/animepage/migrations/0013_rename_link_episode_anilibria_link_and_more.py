# Generated by Django 4.2.7 on 2023-11-20 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0012_episode_n_episode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='link',
            new_name='anilibria_link',
        ),
        migrations.AddField(
            model_name='anime',
            name='anilibria_link',
            field=models.CharField(default=0, max_length=999),
        ),
        migrations.AddField(
            model_name='episode',
            name='kodik_link',
            field=models.CharField(default=0, max_length=999),
        ),
    ]
