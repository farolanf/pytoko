# Generated by Django 2.1.1 on 2018-10-06 02:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('toko', '0012_auto_20181005_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
