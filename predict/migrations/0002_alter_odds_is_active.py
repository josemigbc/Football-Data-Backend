# Generated by Django 4.2.1 on 2023-06-03 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='odds',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]