# Generated by Django 4.2.7 on 2023-12-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0007_remove_comment_film'),
        ('animepage', '0033_remove_filmcomment_film_remove_filmcomment_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalname',
            name='anime',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='anime',
        ),
        migrations.RemoveField(
            model_name='film',
            name='genres',
        ),
        migrations.RenameField(
            model_name='anime',
            old_name='duration',
            new_name='original_title',
        ),
        migrations.RenameField(
            model_name='anime',
            old_name='anilibria_link',
            new_name='player',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='image',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='origin_source',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='status',
        ),
        migrations.AddField(
            model_name='anime',
            name='cover',
            field=models.ImageField(default='images/default.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='anime',
            name='anime_type',
            field=models.CharField(default='ТВ-Серіал', max_length=255),
        ),
        migrations.AlterField(
            model_name='anime',
            name='date_published',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='anime',
            name='description',
            field=models.TextField(default=0, max_length=900),
        ),
        migrations.AlterField(
            model_name='anime',
            name='studio',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='anime',
            name='title',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.DeleteModel(
            name='AdditionalFilmImage',
        ),
        migrations.DeleteModel(
            name='AdditionalName',
        ),
        migrations.DeleteModel(
            name='Episode',
        ),
        migrations.DeleteModel(
            name='Film',
        ),
    ]