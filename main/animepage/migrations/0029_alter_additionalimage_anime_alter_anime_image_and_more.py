# Generated by Django 4.2.7 on 2023-12-08 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0028_additionalimage_delete_additional_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalimage',
            name='anime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animepage.anime'),
        ),
        migrations.AlterField(
            model_name='anime',
            name='image',
            field=models.ImageField(upload_to='anime_covers/'),
        ),
        migrations.CreateModel(
            name='AdditionalFilmImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='additional_images/')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animepage.film')),
            ],
        ),
    ]
