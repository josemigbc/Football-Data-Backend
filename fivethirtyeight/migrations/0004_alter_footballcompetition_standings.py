# Generated by Django 4.2.1 on 2023-07-17 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fivethirtyeight', '0003_rename_competition_footballmatch_league_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballcompetition',
            name='standings',
            field=models.JSONField(blank=True, null=True, verbose_name='standings'),
        ),
    ]
