# Generated by Django 2.0.1 on 2018-01-29 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weeks', '0001_initial'),
        ('home', '0002_auto_20180117_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='last_week',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='last_week', to='weeks.Week'),
            preserve_default=False,
        ),
    ]
