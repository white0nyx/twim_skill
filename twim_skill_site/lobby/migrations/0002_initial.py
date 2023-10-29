# Generated by Django 4.2.5 on 2023-10-29 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lobby', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerlobby',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lobby',
            name='game_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='games.gamemode', verbose_name='Режим игры'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='game_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='games.gametype', verbose_name='Тип игры'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL, verbose_name='Лидер'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='map',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.PROTECT, to='games.map', verbose_name='Карта'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='pool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='games.pool', verbose_name='Пул'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='veto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='games.veto', verbose_name='Вето'),
        ),
    ]
