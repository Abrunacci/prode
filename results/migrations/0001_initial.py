# Generated by Django 2.0.1 on 2018-01-17 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0002_auto_20180115_0158'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weeks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('away_score', models.IntegerField(default=0)),
                ('home_score', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weeks.Week')),
            ],
        ),
    ]
