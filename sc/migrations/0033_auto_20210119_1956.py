# Generated by Django 3.1.3 on 2021-01-19 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0032_cate_pcate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipinfo',
            options={'verbose_name': '访问记录', 'verbose_name_plural': '访问记录'},
        ),
        migrations.AlterModelOptions(
            name='msgbook',
            options={'verbose_name': '用户留言', 'verbose_name_plural': '用户留言'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': '内容详情', 'verbose_name_plural': '内容详情'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '产品详情', 'verbose_name_plural': '产品详情'},
        ),
    ]