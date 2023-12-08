# Generated by Django 4.2.7 on 2023-12-07 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animepage', '0027_additional_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='additional_images/')),
                ('anime', models.ForeignKey(default='/', on_delete=django.db.models.deletion.CASCADE, to='animepage.anime')),
            ],
        ),
        migrations.DeleteModel(
            name='Additional_image',
        ),
    ]