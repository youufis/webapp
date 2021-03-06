# Generated by Django 3.1.3 on 2021-01-27 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sc', '0043_delete_userextend'),
    ]

    operations = [
        migrations.CreateModel(
            name='userextend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.IntegerField(default='104,857,600', verbose_name='存储空间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户资料',
                'verbose_name_plural': '用户资料',
            },
        ),
    ]
