# Generated by Django 4.2.1 on 2023-07-15 03:04

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('logo', models.URLField(blank=True, null=True, verbose_name='url')),
                ('country', models.CharField(max_length=50, verbose_name='country')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('standings', models.JSONField(blank=True, decoder=django.core.serializers.json.Deserializer, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='standings')),
            ],
            options={
                'verbose_name': 'Football Competition',
                'verbose_name_plural': 'Football Competions',
            },
        ),
        migrations.CreateModel(
            name='FootballTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('offensive', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='offensive')),
                ('defensive', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='defensive')),
                ('spi', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='spi')),
                ('logo', models.URLField(blank=True, null=True, verbose_name='url')),
                ('national_league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fivethirtyeight.footballcompetition', verbose_name='Competition')),
            ],
            options={
                'verbose_name': 'Football Team',
                'verbose_name_plural': 'Football Teams',
            },
        ),
        migrations.CreateModel(
            name='FootballMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulltime_home', models.PositiveIntegerField(blank=True, null=True, verbose_name='fulltime_home')),
                ('fulltime_away', models.PositiveIntegerField(blank=True, null=True, verbose_name='fulltime_away')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('prob_home', models.DecimalField(decimal_places=4, max_digits=6, verbose_name='prob_home')),
                ('prob_away', models.DecimalField(decimal_places=4, max_digits=6, verbose_name='prob_away')),
                ('prob_draw', models.DecimalField(decimal_places=4, max_digits=6, verbose_name='prob_draw')),
                ('spi_home', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='spi_away')),
                ('season', models.PositiveIntegerField(verbose_name='season')),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='fivethirtyeight.footballteam')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fivethirtyeight.footballcompetition', verbose_name='competition')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='fivethirtyeight.footballteam')),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
    ]
