# Generated by Django 3.1.3 on 2021-01-18 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0025_auto_20210118_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcate',
            name='slug',
            field=models.SlugField(default='', max_length=40, verbose_name='slug'),
        ),
    ]
