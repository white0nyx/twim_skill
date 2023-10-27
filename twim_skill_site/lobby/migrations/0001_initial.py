# Generated by Django 4.2.5 on 2023-10-27 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet', models.IntegerField(default=0, verbose_name='Ставка')),
                ('password_lobby', models.CharField(max_length=255, null=True, verbose_name='Пароль')),
                ('max_lvl_enter', models.IntegerField(null=True, verbose_name='Максимальный уровень для входа')),
                ('min_lvl_enter', models.IntegerField(null=True, verbose_name='Минимальный уровень для входа')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='SLUG')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerLobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField()),
                ('in_lobby', models.BooleanField()),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lobby', to='lobby.lobby')),
            ],
        ),
    ]
