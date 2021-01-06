# Generated by Django 3.1.3 on 2021-01-05 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sc', '0005_news_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='auditimg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgname', models.CharField(max_length=50, verbose_name='文件名')),
            ],
            options={
                'verbose_name': '图像',
                'verbose_name_plural': '图像',
            },
        ),
        migrations.AlterField(
            model_name='news',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]