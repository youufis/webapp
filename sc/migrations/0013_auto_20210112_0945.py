# Generated by Django 3.1.3 on 2021-01-12 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0012_ipinfo_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newshits',
            options={},
        ),
        migrations.AddField(
            model_name='newshits',
            name='num',
            field=models.IntegerField(blank=True, null=True, verbose_name='次数'),
        ),
    ]
