# Generated by Django 2.0.1 on 2018-01-17 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weeks', '0001_initial'),
        ('standings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weekly',
            name='week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='weeks.Week'),
            preserve_default=False,
        ),
    ]
