# Generated by Django 4.2.7 on 2023-12-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0030_rename_title_additionalname_anime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='date_published',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='film',
            name='description',
            field=models.CharField(default=0, max_length=1500),
        ),
        migrations.AlterField(
            model_name='film',
            name='duration',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='film',
            name='origin_source',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='film',
            name='studio',
            field=models.CharField(default=0, max_length=255),
        ),
    ]