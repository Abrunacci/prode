# Generated by Django 2.0.1 on 2018-01-17 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='current_week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weeks.Week'),
        ),
    ]
