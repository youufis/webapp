# Generated by Django 3.1.3 on 2021-01-27 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0044_userextend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='storage',
            field=models.IntegerField(default='104857600', verbose_name='存储空间'),
        ),
    ]
