# Generated by Django 4.2.5 on 2023-10-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerlobby',
            name='time_enter',
            field=models.DateTimeField(auto_now=True, verbose_name='Время входа'),
        ),
    ]
