# Generated by Django 2.1.2 on 2018-10-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toko', '0016_auto_20181017_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/tmp')),
            ],
        ),
    ]