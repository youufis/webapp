# Generated by Django 3.1.3 on 2020-12-30 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0002_auto_20201224_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='ipinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(default='IP', max_length=20, verbose_name='地址')),
                ('ipaddr', models.GenericIPAddressField(verbose_name='IP地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='日期')),
            ],
            options={
                'verbose_name': '地址',
                'verbose_name_plural': '地址',
            },
        ),
    ]
