# Generated by Django 3.1.3 on 2021-01-18 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0028_auto_20210118_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcate',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, null=True, verbose_name='slug'),
        ),
    ]
