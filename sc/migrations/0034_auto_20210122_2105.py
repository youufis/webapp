# Generated by Django 3.1.3 on 2021-01-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0033_auto_20210119_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='create_date',
        ),
        migrations.AddField(
            model_name='cate',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, null=True, verbose_name='slug'),
        ),
    ]
