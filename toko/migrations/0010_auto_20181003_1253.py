# Generated by Django 2.1.1 on 2018-10-03 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toko', '0009_auto_20181003_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='ad',
        ),
        migrations.AddField(
            model_name='ad',
            name='images',
            field=models.ManyToManyField(to='toko.Image'),
        ),
    ]