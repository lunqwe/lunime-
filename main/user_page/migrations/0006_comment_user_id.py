# Generated by Django 4.2.7 on 2023-12-23 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0005_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
