# Generated by Django 4.2.21 on 2025-05-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_productivenote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='current_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
