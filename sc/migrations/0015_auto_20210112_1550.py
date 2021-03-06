# Generated by Django 3.1.3 on 2021-01-12 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0014_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='repository',
            field=models.CharField(choices=[('无货', '无货'), ('有货', '有货')], default='有货', max_length=10, verbose_name='库存'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('未审核', '未审核'), ('已审核', '已审核')], default='未审核', max_length=10, verbose_name='审核'),
        ),
    ]
