# Generated by Django 3.1.3 on 2021-01-25 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0036_news_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='bconfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='config', max_length=20, verbose_name='网站配置')),
                ('isaudit', models.BooleanField(default=False, verbose_name='是否审核图像')),
                ('isspider', models.BooleanField(default=True, verbose_name='是否抓取外部新闻')),
                ('ismsg', models.BooleanField(default=True, verbose_name='是否开启留言')),
                ('ismsgaudit', models.BooleanField(default=True, verbose_name='是否开启审核留言')),
            ],
            options={
                'verbose_name': '网站配置',
                'verbose_name_plural': '网站配置',
            },
        ),
    ]
