# Generated by Django 4.2.7 on 2023-11-30 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0024_film_anilibria_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='date_published',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='anime',
            name='description',
            field=models.CharField(max_length=950),
        ),
        migrations.AlterField(
            model_name='film',
            name='description',
            field=models.CharField(max_length=950),
        ),
    ]
