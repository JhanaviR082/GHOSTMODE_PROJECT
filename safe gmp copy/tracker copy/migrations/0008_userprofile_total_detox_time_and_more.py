# Generated by Django 4.2.20 on 2025-05-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_remove_badge_criteria_remove_badge_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_detox_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='current_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longest_streak',
            field=models.IntegerField(default=0),
        ),
    ]
